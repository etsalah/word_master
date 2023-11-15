from app.setup import get_settings

from flask import Blueprint, request, flash, redirect, url_for, current_app
from flask import render_template

from app.v1.database.models.tag import Tag
from app.v1.routes.tag.forms.form import CreateForm, EditForm
from app.v1.helpers import id_helpers

app_settings = get_settings()

app = app_settings['app']
db = app_settings['db_manager']

bp = Blueprint('tag_v1', __name__, template_folder="templates")


@bp.get('/')
def tag():
    tag_list = db.paginate(db.select(Tag))
    return render_template("tag/tags.html", tag_list=tag_list)


@bp.route('/create', methods=['POST', 'GET'])
def create_tag():
    form = CreateForm()
    if request.method == "GET":
        print("create form reached")
        return render_template("tag/create.html", form=form)
    elif request.method == "POST" and form.validate_on_submit():
        tag = Tag(id=id_helpers.generate_id(), tag=form.tag.data)
        db.session.add(tag)
        try:
            db.session.commit()
            flash("The tag has been save successfully", category="success")
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
            flash(
                "An error occurred will saving the tag. Kindly try again later",
                category="error")
        return redirect(url_for("tag_v1.create_tag"))
    elif request.method == "POST" and not form.validate_on_submit():
        flash("\n".join(form.errors), category="error")
        return redirect(url_for("tag_v1.create_tag"))

    flash(
        f"`{request.method}` request aren't currently supported",
        category="error")
    return redirect(url_for("tag_v1.tag"))


@bp.route('/<tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    form = EditForm()
    tag_obj = db.session.execute(
        db.select(Tag).filter_by(tag_id=tag_id)).scalar_one()
    
    if request.method == "GET":
        return render_template("tag/edit.html", form=form, tag_obj=tag_obj)
    elif request.method == "POST" and form.validate_on_submit():
        tag_obj.tag = str(form.tag.data).strip()
        db.session.add(tag_obj)
        try:
            db.session.commit()
            flash("The tag has been update. Successfully", category="success")
            return redirect(url_for("tag_v1.edit_tag", tag_id=tag_id))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            current_app.logger.error("Update")
            flash(
                "An error occurred whilst trying to update the tag. "
                "Try again later", category="error")
            return redirect(url_for("tag_v1.edit_tag", tag_id=tag_id))
    elif request.method == "POST" and not form.validate_on_submit():
        msg = "\n".join(form.errors)
        current_app.logger.error(msg)
        flash(msg, category="error")
        return redirect(url_for("tag_v1.edit_tag", tag_id=tag_id))

    flash(
        f"`{request.method}` request aren't currently supported",
        category="error"
    )
    return redirect(url_for("tag_v1.edit_tag"))


@bp.route("/<tag_id>/view", methods=["GET", ])
def view_tag(tag_id):
    tag_obj = db.session.execute(
        db.select(Tag).filter_by(tag_id=tag_id)).scalar_one()
    if not tag_obj:
        msg = "No tag was found with the provide id"
        flash(msg, category="info")
        current_app.logger.error(f"{msg} `{tag_id}`")
        return redirect(url_for("tag_v1.tag"))
    
    return render_template("tag/view.html", tag_obj=tag_obj)
