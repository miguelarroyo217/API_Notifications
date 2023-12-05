from logger.logger import log
from flask import jsonify
from datetime import datetime

class NotifService:
    def __init__(self, db_connector):
        self.db_connector = db_connector


    def get_all_due_tasks(self):
        try:
            """ 0 to hide and 1 to show attribute """
            self.tasks = list(self.db_connector.db.tasks.find({},{
                '_id': 0, 
                'tasks.name': 1,
                'tasks.due': 1, 
                'tasks.notifications': 1
                }))
            
            self.due_tasks = list()
            for list_tasks in self.tasks:
                for task in list_tasks.values():
                    for due_task in task:
                        self.due_tasks.append(due_task)

            self.due_tasks = sorted(self.due_tasks, key=lambda task:datetime.strptime(task['due'],"%Y-%m-%d %H:%M:%S"))
            return self.due_tasks
        except Exception as e:
            log.critical(f'Error fetching all tasks from the database: {e}')
            return jsonify({'error': f'Error fetching all tasks from the database: {e}'}), 500
        
    
    def get_notif_by_id(self, list_id, task_id, notif_id):
        try:
            self.notif = self.db_connector.db.tasks.find_one({
                '_id': list_id,
                'tasks._id': task_id,
                'tasks.notifications._id': notif_id
                })
            
            """ for task in self.notif['tasks']:
                if task['_id'] == task_id:
                    for notif_task in task['notifications']:
                        if notif_task['_id'] == notif_id:
                            return list(notif_task) """
    
            return self.notif
        except Exception as e:
            log.critical(f'Error fetching the notification id from the database: {e}')
            return jsonify({'error': f'Error fetching the notification id from the database: {e}'}), 500

