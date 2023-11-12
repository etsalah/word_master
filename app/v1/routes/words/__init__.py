from app.setup import get_settings

from flask import Blueprint
from flask import render_template

from app.v1.database.models.word import Word

app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']

bp = Blueprint('word_v1', __name__, template_folder="templates")

@bp.get('/')
def word():
    word_list = db.paginate(db.select(Word))
    return render_template("words.html", word_list=word_list)
