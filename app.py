from flask import Flask
from models.notifications_models import NotifModel
from flask_swagger_ui import get_swaggerui_blueprint
from services.notifications_services import NotifService
from routes.notifications_routes import NotifRoutes
from schemas.notifications_schemas import NotifSchema
from flask_cors import CORS

app = Flask(__name__)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db_connector = NotifModel()
db_connector.connect_to_database()

notif_service = NotifService(db_connector)
notif_schema = NotifSchema()

notif_blueprint = NotifRoutes(notif_service, notif_schema)
app.register_blueprint(notif_blueprint)

CORS(app, resources={r'/api/notifications': {'origins': 'http://localhost:3000'}})

if __name__ == '__main__':
    try:
        app.run(debug=True)
    finally:
        db_connector.close_connection()