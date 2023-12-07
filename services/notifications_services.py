from logger.logger import log
from flask import jsonify
from datetime import datetime

class NotifService:
    def __init__(self, db_connector):
        self.db_connector = db_connector


    def get_all_tasks(self):
        try:           
            self.tasks = list(self.db_connector.db.task_lists.find())
            self.due_tasks = list()
            for list_t in self.tasks:
                for task in list_t['tasks']:
                    if task['status'] == 'Pending':
                        self.due_tasks.append({
                            'list_id': list_t['_id'],
                            'task_id': task['_id'],
                            'name': task['name'],
                            'due': task['due'],
                            'status': task['status']
                        })
            self.due_tasks = sorted(self.due_tasks, key=lambda task:datetime.strptime(task['due'],"%Y-%m-%d %H:%M:%S"))
            return self.due_tasks
        except Exception as e:
            log.critical(f'Error fetching all tasks from the database: {e}')
            return jsonify({'error': f'Error fetching all tasks from the database: {e}'}), 500
        
    
    def get_task_by_id(self, list_id, task_id):
        try:
            self.notif = self.db_connector.db.task_lists.find_one({
                '_id': list_id,
                'tasks._id': task_id
                })
            self.due_task = list()
            for task in self.notif['tasks']:
                if task['_id'] == task_id:
                    self.due_task.append({
                        'list_id': list_id,
                        'task_id': task_id,
                        'name': task['name'],
                        'due': task['due'],
                        'status': task['status']
                    })
            return self.due_task
        except Exception as e:
            log.critical(f'Error fetching the notification id from the database: {e}')
            return jsonify({'error': f'Error fetching the notification id from the database: {e}'}), 500

    def update_due_task(self, list_id, task_id, updated_due):
        try:
            updated_notif = self.get_task_by_id(list_id, task_id)
            if updated_notif:
                result = self.db_connector.db.task_lists.update_one({
                '_id': list_id,
                'tasks._id': task_id,
                },
                {'$set': {'tasks.$.due': updated_due}})
                if result.modified_count > 0:
                    return updated_notif
                else:
                    return {'message': 'The notifications is already up-to-date'}
            else:
                return None
        except Exception as e:
            log.critical(f'Error updating the notification due: {e}')
            return jsonify({'error': f'Error updating the notification due: {e}'}), 500
        
    def delete_task(self, list_id, task_id):
        try:
            deleted_task = self.get_task_by_id(list_id, task_id)
            if deleted_task:
                self.db_connector.db.task_lists.update_one({
                '_id': list_id,
                'tasks._id': task_id},
                {'$unset': {'tasks.$._id': 1, 'tasks.$.name': 1,
                            'tasks.$.description': 1, 'tasks.$.due': 1,
                            'tasks.$.status': 1, 'tasks.$.notifications': 1}})
                return deleted_task
            else:
                return None
        except Exception as e:
            log.critical(f'Error deleting the task: {e}')
            return jsonify({'error': f'Error deleting the task: {e}'}), 500