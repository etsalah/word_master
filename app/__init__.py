
from app import setup

APP_SETTINGS = setup.create_app()

app = APP_SETTINGS['app']
db_manager = APP_SETTINGS['db_manager']
migrate = APP_SETTINGS['migrate']

from app.v1.routes.words import bp as word_v1_bp
from app.v1.routes.dashboard import bp as dashboard_v1_bp

blueprint_mappings = (
    (word_v1_bp, '/word'),
    (dashboard_v1_bp, '/'),
)
setup.register_blueprints(app, blueprint_mappings)
