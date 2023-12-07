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
        self.route('/apinotif/notif', methods=['GET'])(self.get_task_list)

        """ ids: task-list, task, notification """
        self.route('/apinotif/notif/<int:list_id>/<int:task_id>/<int:notif_id>', methods=['GET'])(self.get_notif_by_id)
        
        self.route('/apinotif/notif/<int:list_id>/<int:task_id>/<int:notif_id>', methods=['PUT'])(self.update_due_notif)

        """ self.route('/apinotif/notif', methods=['POST'])(self.add_notif)

        self.route('/apinotif/notif/<int:notif_id>', methods=['DELETE'])(self.delete_notif) """

    def get_task_list(self):
        try:
            self.notif = self.notif_service.get_all_due_tasks()
            return jsonify(self.notif), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
    
    def get_notif_by_id(self, list_id, task_id, notif_id):
        try:
            self.notif = self.notif_service.get_notif_by_id(list_id, task_id, notif_id)
            if self.notif:
                return jsonify(self.notif), 200
            else: 
                return jsonify({'error': 'Notification not found'}), 404
        except Exception as e:
            log.exception(f'Error fetching notification by id from the database: {e}')
            return jsonify({'error': 'Failed to fetch notification by id from the database'}), 500
        
    def update_due_notif(self, list_id, task_id, notif_id):
        try:
            self.data=request.json
            log.info(self.data)
            if not self.data:
                    return jsonify({'error': 'Invalid data'}), 400

            self.due_notif = self.data.get('due_notif')

            self.notif = self.notif_service.update_due_notif(list_id, task_id, notif_id, self.due_notif)
            if self.notif:
                return jsonify(self.notif), 200
            else: 
                return jsonify({'error': 'Notification not found'}), 404
        except Exception as e:
            log.exception(f'Error updating due notification: {e}')
            return jsonify({'error': 'Error updating due notification'}), 500
        
    """ def add_notif(self):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.author = self.data.get('author')

            try:
                self.notif_schema.validate_title(self.title)
                self.notif_schema.validate_author(self.author)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.new_notif = {
                'title': self.title,
                'author': self.author
            }

            self.created_notif = self.notif_service.add_notif(self.new_notif)
            return jsonify(self.created_notif), 201
        except Exception as e:
            log.critical(f'Error adding a new notification to the database: {e}')

    def update_notif(self, notif_id):
        try:
            self.data = request.json
            if not self.data:
                return jsonify({'error': 'Invalid data'}), 400
            
            self.title = self.data.get('title')
            self.author = self.data.get('author')

            try:
                self.notif_schema.validate_title(self.title)
                self.notif_schema.validate_author(self.author)
            except ValidationError as e:
                 return(jsonify({'error': 'Invalid data', 'details': e.messages}), 400)
            
            self.notif_updated = self.notif_service.update_notif(notif_id, self.data)

            if self.notif_updated:
                return jsonify(self.notif_updated), 200
            else:
                return jsonify({'error': 'notification not found'}), 404

        except Exception as e:
            log.critical(f'Error updating the notification in the database: {e}')

    def delete_notif(self, notif_id):
        try:
            self.notif_deleted = self.notif_service.delete_notif(notif_id)
            if self.notif_deleted:
                return jsonify(self.notif_deleted), 200
            else:
                return jsonify({'error': 'notification not found'}), 404
        except Exception as e:
            log.critical(f'Error deleting the notification in the database: {e}')
 """