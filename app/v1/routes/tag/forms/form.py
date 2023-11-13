from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    tag = StringField(
        "Tag Name", validators=[
            DataRequired(
                "You need to provide the name of the tag you want to create"),
            ])


class EditForm(FlaskForm):
    tag = StringField(
        "Tag Name", validators=[
            DataRequired(
                "You need to provide the name of the tag you want to create"),
        ]
    )
