from flask import Blueprint, jsonify, request
from logger.logger import log
from marshmallow import ValidationError

class NotifRoutes(Blueprint):
    def __init__(self, notif_service, notif_schema):
        super().__init__('notif', __name__)
        self.notif_service = notif_service
        self.notif_schema = notif_schema
        self.register_routes()

    def register_routes(self):
        """ READ """
        self.route('/apinotif/notif', methods=['GET'])(self.get_all_tasks)

        """ ids: task-list, task, notification """
        self.route('/apinotif/notif/<int:list_id>/<int:task_id>', methods=['GET'])(self.get_task_by_id)
        
        self.route('/apinotif/notif/<int:list_id>/<int:task_id>', methods=['PUT'])(self.update_due_task)

        self.route('/apinotif/notif/<int:list_id>/<int:task_id>', methods=['DELETE'])(self.delete_task)

        """ self.route('/apinotif/notif', methods=['POST'])(self.add_notif) """

    def get_all_tasks(self):
        try:
            self.notif = self.notif_service.get_all_tasks()
            return jsonify(self.notif), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
    
    def get_task_by_id(self, list_id, task_id):
        try:
            self.notif = self.notif_service.get_task_by_id(list_id, task_id)
            if self.notif:
                return jsonify(self.notif), 200
            else: 
                return jsonify({'error': 'Notification not found'}), 404
        except Exception as e:
            log.exception(f'Error fetching notification by id from the database: {e}')
            return jsonify({'error': 'Failed to fetch notification by id from the database'}), 500
        
    def update_due_task(self, list_id, task_id):
        try:
            self.data=request.json
            self.data = request.json
            log.info(self.data)
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.due_notif = self.data.get('due')
            
            try:
                self.notif_schema.validate_due(self.due_notif)
            except ValidationError as e:
                return(jsonify({'error': 'Invalid data date', 'details': e.messages}), 400)
            
            self.notif = self.notif_service.update_due_task(list_id, task_id, self.due_notif)
            if self.notif:
                return jsonify(self.notif), 200
            else: 
                return jsonify({'error': 'Notification not found'}), 404
        except Exception as e:
            log.exception(f'Error updating due notification: {e}')
            return jsonify({'error': 'Error updating due notification'}), 500
    
    def delete_task(self, list_id, task_id):
        try:
            self.task_deleted = self.notif_service.delete_task(list_id, task_id)
            if self.task_deleted:
                return jsonify(self.task_deleted), 200
            else:
                return jsonify({'error': 'Task not found'}), 404
        except Exception as e:
            log.exception(f'Error deleting the task in the database: {e}')
            return jsonify({'error': 'Error deleting the task in the database'}), 500