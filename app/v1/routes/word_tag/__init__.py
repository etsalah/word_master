from sqlalchemy.exc import IntegrityError
from flask import Blueprint, request, flash, redirect, url_for, current_app
from flask import render_template

from app.setup import get_settings

from app.v1.database.models.word_tag import WordTag
from app.v1.database.models.word import Word
from app.v1.database.models.tag import Tag
from app.v1.database.views.word_tag_list import VwWordTagList

from app.v1.routes.word_tag.forms.form import CreateForm, EditForm, BulkForm
from app.v1.helpers import id_helpers
from app.v1.routes.word_tag import helper as word_tag_helper


app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']

bp = Blueprint('word_tag_v1', __name__, template_folder="templates")


@bp.get('/<word_id>')
@bp.get('/<word_id>/')
@bp.get('/<word_id>/<word_group>')
@bp.get('/<word_id>/<word_group>/')
@bp.get('/<word_id>/<word_page>')
@bp.get('/<word_id>/<word_page>/<word_group>')
@bp.get('/<word_id>/<word_page>/<word_group>/')
def word_tag(word_id, word_page=None, word_group=None):
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
    template_context = {
        "word_id": word_id, "word": word_obj,  "word_tag_list": word_tag_list,
        "available_tag_list": available_tag_list, "form": form
    }

    if word_group:
        template_context['word_group'] = word_group

    if word_page:
        template_context['word_page'] = word_page
        
    return render_template("word_tag/word_tag.html", **template_context)


@bp.route('/create/<action>/bulk', methods=['POST', ])
@bp.route('/create/<action>/bulk/', methods=['POST', ])
@bp.route('/create/<action>/bulk/<word_page>', methods=['POST', ])
@bp.route('/create/<action>/bulk/<word_page>/', methods=['POST', ])
@bp.route('/create/<action>/bulk/<word_page>/<word_group>', methods=['POST', ])
@bp.route('/create/<action>/bulk/<word_page>/<word_group>', methods=['POST', ])
@bp.route('/create/<action>/bulk/<word_page>/<word_group>/', methods=['POST', ])
def bulk_word_tag(action, word_page=None, word_group=None):
    form = BulkForm()
    
    word_group = request.args.get('word_group', None) if not word_group else word_group

    if request.method == "POST" and action == "edit":
        choosen_words_str = form.choosen_words.data.strip()
        choosen_words_lst = word_tag_helper.process_choosen_word_str(
            choosen_words_str)
        
        common_tags_set = word_tag_helper.get_common_tag_lst(
            db, choosen_words_lst)

        available_tag_list = db.session.execute(
            db.Select(Tag)
        ).scalars()

        template_context = {
            "choosen_words_str": choosen_words_str,
            "choosen_words": choosen_words_lst,
            "available_tag_list": available_tag_list,
            "common_tags": common_tags_set, "form": form,
            "word_page": word_page, "word_group": word_group
        }
        return render_template(
            "word_tag/bulk_word_tag.html", **template_context)
    elif request.method == "POST" and action == "create" and form.validate_on_submit():
        choosen_words_str = form.choosen_words.data.strip()
        choosen_words_lst = word_tag_helper.process_choosen_word_str(
            choosen_words_str)
        words = []
        for choosen_word in choosen_words_lst:    
            word_tag_obj = WordTag(
                word_tag_id=id_helpers.generate_id(), word_id=choosen_word[0],
                tag_id=form.tag_id.data.strip(),
                description=form.description.data.strip()
            )
            db.session.add(word_tag_obj)
            words.append(choosen_word[2])
            try:
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
            except Exception as e:
                current_app.logger.error(e)

        flash(
            f"Tag has been applied to {', '.join(words)}, successfully",
            category="success")
        
        available_tag_list = word_tag_helper.get_available_tags(db)
        common_tags_set = word_tag_helper.get_common_tag_lst(
            db, choosen_words_lst)
        template_context = {
            "choosen_words_str": choosen_words_str,
            "choosen_words": choosen_words_lst,
            "available_tag_list": available_tag_list,
            "common_tags": common_tags_set, "form": form,
            "word_page": word_page, "word_group": word_group
        }
        return render_template(
            "word_tag/bulk_word_tag.html", **template_context)
    
    elif request.method == "POST" and action == "create" and not form.validate_on_submit():
        flash(",".join(form.errors), category="error")
        choosen_words_str = form.choosen_words.data.strip()
        choosen_words_lst = word_tag_helper.process_choosen_word_str(
            choosen_words_str)
        available_tag_list = word_tag_helper.get_available_tags(db)
        common_tags_set = word_tag_helper.get_common_tag_lst(
            db, choosen_words_lst)
        template_context = {
            "choosen_words_str": choosen_words_str,
            "choosen_words": choosen_words_lst,
            "available_tag_list": available_tag_list,
            "common_tags": common_tags_set, "form": form,
            "word_page": word_page, "word_group": word_group
        }
        return render_template(
            "word_tag/bulk_word_tag.html", **template_context)
    
    flash(
        f"The `{request.method}` method is currently not supported",
        category="error")
    
    if word_page and word_group:
        return redirect(
            url_for("word_v1.word", word_page=word_page, word_group=word_group))
    elif word_page and not word_group:
        return redirect(url_for("word_v1.word", word_page=word_page))
    elif not word_page and word_group:
        return redirect(url_for("word_v1.word", word_group=word_group))

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


@bp.route(
    '/<word_id>/<word_tag_id>/edit/<page>/<word_group>',
    methods=['GET', 'POST'])
@bp.route(
    '/<word_id>/<word_tag_id>/edit<page>/<word_group>/',
    methods=['GET', 'POST'])
def edit_word_tag(word_id, word_tag_id, page=None, word_group=None):
    form = EditForm()
    word_tag_obj = db.session.execute(
        db.select(WordTag).filter_by(word_tag_id=word_tag_id)).scalar_one()
    

    def _get_context():
        context = {
            "form": form, "word_id": word_id, "word_tag_id": word_tag_id,
            "word_tag_obj": word_tag_obj}

        if page:
            context["page"] = page

        if word_group:
            context["word_group"] = word_group

        return context


    if request.method == "GET":
        template_context = _get_context()

        return render_template("word_tag/edit.html", **template_context)
    
    elif request.method == "POST" and form.validate_on_submit():

        context = _get_context()

        word_tag_obj.tag_id = str(form.tag_id.data).strip()
        word_tag_obj.description = str(form.description.data).strip()
        db.session.add(word_tag_obj)
        try:
            db.session.commit()
            flash(
                "The word tag has been update. Successfully",
                category="success")
            return redirect(url_for("word_tag_v1.edit_word_tag", **context))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            current_app.logger.error("Update")
            flash(
                "An error occurred whilst trying to update the tag. "
                "Try again later", category="error")
            return redirect(url_for("word_tag_v1.edit_word_tag", **context))
        
    elif request.method == "POST" and not form.validate_on_submit():
        msg = "\n".join(form.errors)
        current_app.logger.error(msg)
        flash(msg, category="error")
        context = _get_context()
        return redirect(url_for("word_tag_v1.edit_word_tag", **context))

    flash(
        f"`{request.method}` request aren't currently supported",
        category="error"
    )
    return redirect(url_for("word_tag_v1.edit_word_tag", **_get_context()))


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
    