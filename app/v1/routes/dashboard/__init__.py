from copy import deepcopy
from flask import Blueprint, render_template

from app.v1.database.views.tag_word_count import VwTagWordCount
from app.setup import get_settings

app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']


bp = Blueprint("dashboard_v1", __name__, template_folder="./templates")


@bp.get('/', )
def dashboard():
    tag_word_count_ls = db.session.execute(
        db.select(
            VwTagWordCount.tag_id, VwTagWordCount.tag,
            VwTagWordCount.word_count))
    word_grouping = []
    tmp = []
    for tag in tag_word_count_ls:
        tmp.append(tag)
        if len(tmp) == 4:
            word_grouping.append(deepcopy(tmp))
            tmp.clear()
    return render_template(
        'dashboard/dashboard.html', tag_word_list=word_grouping)
