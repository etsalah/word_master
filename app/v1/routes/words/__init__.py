from app.setup import get_settings

from flask import Blueprint, render_template, request, redirect, url_for

from app.v1.database.models.word import Word
from app.v1.routes.word_tag.forms.form import BulkForm
from app.v1.database.views.word_length_group import VwWordLengthGroup

app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']

bp = Blueprint(
    'word_v1', __name__, template_folder="templates",
    static_folder="static")


@bp.get('/')
def word():
    word_group_length = request.args.get('word_group', None)
    word_groups = db.session.execute(
        db.select(VwWordLengthGroup.word_count, VwWordLengthGroup.word_length)
    ).all()
    page = request.args.get('page', None)
    form = BulkForm()
    if word_group_length and word_group_length != "all":
        try:
            word_group_length = int(word_group_length)
        except ValueError:
            return redirect(url_for("word_v1.word"))
        
        word_list = db.paginate(
            db.select(Word).filter(
                Word.length==int(word_group_length)
            ).order_by(Word.length.asc(), Word.word.asc()))
        context = {
            "word_list": word_list, "form": form,
            "selected_word_group": word_group_length,
            "word_groups": word_groups, "word_page": page
        }
        return render_template("words/words.html", **context)
    else:
        word_list = db.paginate(db.select(Word))
        context = {
            "word_list": word_list, "form": form,
            "selected_word_group": word_group_length,
            "word_groups": word_groups, "word_page": page
        }
        return render_template("words/words.html", **context)
