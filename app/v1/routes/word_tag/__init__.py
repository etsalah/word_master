from app.setup import get_settings

from flask import Blueprint, request, flash, redirect, url_for, current_app
from flask import render_template

from app.v1.database.models.word_tag import WordTag
from app.v1.database.models.word import Word
from app.v1.database.models.tag import Tag
from app.v1.database.views.word_tag_list import VwWordTagList

from app.v1.routes.word_tag.forms.form import CreateForm, EditForm, BulkForm
from app.v1.helpers import id_helpers

app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']

bp = Blueprint('word_tag_v1', __name__, template_folder="templates")


@bp.get('/<word_id>')
@bp.get('/<word_id>/')
def word_tag(word_id):
    word_obj = db.session.execute(
        db.Select(Word).filter(Word.word_id==word_id)
    ).scalar()

    if not word_obj:
        flash(f"No word was found with id {word_id}", category="error")
        return redirect(url_for("word_v1.word"))
    
    tag_list_stmt = db.select(VwWordTagList).filter(
        VwWordTagList.word_id==word_id)

    word_tag_list = db.paginate(tag_list_stmt)

    all_word_tags = db.session.execute(
        db.Select(WordTag.tag_id).filter(WordTag.word_id==word_id)
    ).scalars()

    available_tag_select_stmt = db.Select(Tag).filter(
        Tag.tag_id.notin_(all_word_tags))
    available_tag_list = db.session.execute(
        available_tag_select_stmt
    ).scalars()

    form = CreateForm()
    return render_template(
        "word_tag/word_tag.html", **{
            "word_id": word_id, "word": word_obj,
            "word_tag_list": word_tag_list,
            "available_tag_list": available_tag_list,
            "form": form,
        })


@bp.route('/create/<action>', methods=['POST', ])
@bp.route('/create/<action>/', methods=['POST', ])
def bulk_word_tag(action):
    form = BulkForm()
    if request.method == "POST" and action == "edit" and form.validate_on_submit():
        choosen_words_str = form.choosen_words.data.strip()
        choosen_words_lst = [
            choosen_word.split("$$")
            for choosen_word in choosen_words_str.split(",")
        ]
        
        word_tag_list = db.session.execute(db.select(Tag.tag_id, Tag.tag)).all()

        return render_template(
            "word_tag/bulk_word_tag.html", **{
                "choosen_words_str": choosen_words_str,
                "choosen_words": choosen_words_lst,
                'available_tag_list': word_tag_list,
                'form': form,
            })
    elif request.method == "POST" and not form.validate_on_submit():
        flash("You need to select some words to tag", category="info")
        return redirect(url_for("word_v1.word"))
    elif request.method == "POST" and action == "create" and form.validate_on_submit():
        pass

    flash(
        f"The `{request.method}` method is currently not supported",
        category="error")
    return redirect(url_for("word_v1.word"))


@bp.route('/create/<word_id>', methods=['POST', ])
@bp.route('/create/<word_id>/', methods=['POST', ])
def create_word_tag(word_id):
    word_obj = db.session.execute(
        db.Select(Word).filter(Word.word_id==word_id)
    ).scalar()

    if not word_obj:
        flash(f"No word was found with id {word_id}", category="error")
        return redirect(url_for("word_v1.word"))
    
    form = CreateForm()
    if request.method == "POST" and form.validate_on_submit():
        word_tag = WordTag(
            word_tag_id=id_helpers.generate_id(),
            word_id=word_id,
            tag_id=str(form.tag_id.data).strip(),
            description=str(form.description.data).strip()
        )
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
        return redirect(url_for("word_tag_v1.word_tag", word_id=word_id))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("\n".join(form.errors), category="error")
        return redirect(url_for("word_tag_v1.word_tag", word_id=word_id))

    flash(
        f"`{request.method}` request aren't currently supported",
        category="error")
    return redirect(url_for("word_tag_v1.word_tag", word_id=word_id))


@bp.route('/<word_id>/<word_tag_id>/edit', methods=['GET', 'POST'])
def edit_word_tag(word_id, word_tag_id):
    form = EditForm()
    word_tag_obj = db.session.execute(
        db.select(WordTag).filter_by(word_tag_id=word_tag_id)).scalar_one()
    
    if request.method == "GET":
        return render_template(
            "word_tag/edit.html", form=form, word_tag_obj=word_tag_obj)
    elif request.method == "POST" and form.validate_on_submit():
        word_tag_obj.tag_id = str(form.tag_id.data).strip()
        word_tag_obj.description = str(form.description.data).strip()
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


@bp.route("/<word_tag_id>/delete", methods=["GET", ])
@bp.route("/<word_tag_id>/delete/", methods=["GET", ])
def delete_word_tag(word_tag_id):
    word_tag_obj = db.session.execute(
        db.Select(WordTag).filter_by(word_tag_id=word_tag_id)
    ).scalar_one()

    if not word_tag_obj:
        msg = "No word tag was found with the provide id"
        flash(msg, category="info")
        current_app.logger.error(f"{msg} `{word_tag_id}`")
        return redirect(url_for("word_v1.word"))

    db.session.delete(word_tag_obj)
    try:
        word_id = word_tag_obj.word_id
        db.session.commit()
        msg = "Word Tag has been delete successfully"
        flash(msg, category="success")
        current_app.logger.info(msg)
        return redirect(url_for("word_tag_v1.word_tag", word_id=word_id))
    except Exception as e:
        db.session.rollback()
        flash("An unexpected error, kindly try again later", category="error")
        current_app.logger.info(e)
        return redirect(url_for("word_tag_v1.word_tag", word_id=word_id))
    