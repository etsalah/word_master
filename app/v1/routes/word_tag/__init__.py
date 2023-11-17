from app.setup import get_settings

from flask import Blueprint, request, flash, redirect, url_for, current_app
from flask import render_template

from app.v1.database.models.word_tag import WordTag
from app.v1.database.models.word import Word
from app.v1.database.models.tag import Tag

from app.v1.routes.tag.forms.form import CreateForm, EditForm
from app.v1.helpers import id_helpers

app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']

bp = Blueprint('word_tag_v1', __name__, template_folder="templates")


@bp.get('/<word_id>')
@bp.get('/<word_id>/')
def word_tag(word_id):
    word_tag_list = db.paginate(
        db.select(WordTag.word_tag_id, Tag.tag).join(
            Tag, Tag.tag_id==WordTag.tag_id
        ).filter(WordTag.word_id==word_id))
    return render_template(
        "word_tag/word_tag.html", word_id=word_id, word_tag_list=word_tag_list)


@bp.route('/create/<word_id>', methods=['POST', 'GET'])
@bp.route('/create/<word_id>/', methods=['POST', 'GET'])
def create_word_tag():
    form = CreateForm()
    if request.method == "GET":
        print("create form reached")
        return render_template("word_tag/create.html", form=form)
    elif request.method == "POST" and form.validate_on_submit():
        word_tag = WordTag(word_tag_id=id_helpers.generate_id(), tag=form.tag.data)
        db.session.add(word_tag)
        try:
            db.session.commit()
            flash("The word tag has been save successfully", category="success")
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            flash(
                "An error occurred will saving the tag. Kindly try again later",
                category="error")
        return redirect(url_for("word_tag_v1.create_word_tag"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("\n".join(form.errors), category="error")
        return redirect(url_for("word_tag_v1.create_word_tag"))

    flash(
        f"`{request.method}` request aren't currently supported",
        category="error")
    return redirect(url_for("word_tag_v1.word_tag"))


@bp.route('/<word_id>/<word_tag_id>/edit', methods=['GET', 'POST'])
def edit_word_tag(word_id, word_tag_id):
    form = EditForm()
    word_tag_obj = db.session.execute(
        db.select(WordTag).filter_by(word_tag_id=word_tag_id)).scalar_one()
    
    if request.method == "GET":
        return render_template(
            "word_tag/edit.html", form=form, word_tag_obj=word_tag_obj)
    elif request.method == "POST" and form.validate_on_submit():
        word_tag_obj.tag = str(form.tag.data).strip()
        db.session.add(word_tag_obj)
        try:
            db.session.commit()
            flash(
                "The word tag has been update. Successfully",
                category="success")
            return redirect(
                url_for(
                    "word_tag_v1.edit_word_tag", word_id=word_id,
                    word_tag_id=word_tag_id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            current_app.logger.error("Update")
            flash(
                "An error occurred whilst trying to update the tag. "
                "Try again later", category="error")
            return redirect(
                url_for(
                    "word_tag_v1.edit_word_tag", word_id=word_id,
                    word_tag_id=word_tag_id))
    elif request.method == "POST" and not form.validate_on_submit():
        msg = "\n".join(form.errors)
        current_app.logger.error(msg)
        flash(msg, category="error")
        return redirect(
            url_for(
                "word_tag_v1.edit_word_tag", word_tag_id=word_tag_id))

    flash(
        f"`{request.method}` request aren't currently supported",
        category="error"
    )
    return redirect(url_for("word_tag_v1.edit_word_tag"))


@bp.route("/<word_id>/<word_tag_id>/view", methods=["GET", ])
@bp.route("/<word_id>/<word_tag_id>/view/", methods=["GET", ])
def view_word_tag(word_id, word_tag_id):
    tag_obj = db.session.execute(
        db.select(WordTag).filter_by(word_tag_id=word_tag_id)).scalar_one()
    if not tag_obj:
        msg = "No tag was found with the provide id"
        flash(msg, category="info")
        current_app.logger.error(f"{msg} `{word_tag_id}`")
        return redirect(url_for("word_tag_v1.word_tag"))
    
    return render_template("word_tag/view.html", tag_obj=tag_obj)
