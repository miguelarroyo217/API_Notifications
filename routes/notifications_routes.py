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
        self.route('/api/notif', methods=['GET'])(self.get_notif)
        self.route('/api/notif/<int:notif_id>', methods=['GET'])(self.get_notif_by_id)
        """ CREATE """
        self.route('/api/notif', methods=['POST'])(self.add_notif)
        """ UPDATE """
        self.route('/api/notif/<int:notif_id>', methods=['PUT'])(self.update_notif)
        """ DELETE """
        self.route('/api/notif/<int:notif_id>', methods=['DELETE'])(self.delete_notif)

    def get_notif(self):
        try:
            self.notif = self.notif_service.get_all_notif()
            return jsonify(self.notif), 200
        except Exception as e:
            log.exception(f'Error fetching data from the database: {e}')
            return jsonify({'error': 'Failed to fetch data from the database'}), 500
    
    def get_notif_by_id(self, notif_id):
        self.notif = self.notif_service.get_notif_by_id(notif_id)
        if self.notif:
            return jsonify(self.notif), 200
        else: 
            return jsonify({'error': 'Notification not found'}), 404
        
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