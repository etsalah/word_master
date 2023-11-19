import os, sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
sys.path.insert(0, os.path.abspath('.'))

BASE_DIR = os.path.abspath('.')

APP_CONFIG = {}

def create_app():
    global APP_CONFIG

    if APP_CONFIG:
        return APP_CONFIG
    
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)
    db_manager = SQLAlchemy(app)
    migrate = Migrate(app, db_manager)
    APP_CONFIG = {
        "app": app, "db_manager": db_manager, "migrate": migrate
    }
    return APP_CONFIG


def register_blueprints(app_obj, blueprint_maps):
    for route in blueprint_maps:
        app_obj.register_blueprint(route[0], url_prefix=route[1])


def get_settings():
    global APP_CONFIG
    if not APP_CONFIG:
        create_app()
    return APP_CONFIG
