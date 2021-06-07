import sys
import os
import werkzeug
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from dateutil import parser

sys.path.insert(0, os.path.abspath('.'))

BASE_DIR = os.path.abspath('.')

app = Flask(__name__, template_folder="templates")

from config import Config

app.config.from_object(Config)
db_manager = SQLAlchemy(app)
migrate = Migrate(app, db_manager)
