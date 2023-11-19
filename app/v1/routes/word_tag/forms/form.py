from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    tag_id = StringField(
        "tag_id", validators=[
            DataRequired(
                "You need to provide the tag_id that you want to add to the "
                "word"
            ),
        ]
    )
    description = StringField(
        "Description", validators=[
            DataRequired(
                "You need to provide the name of the tag you want to create"),
            ])


class EditForm(FlaskForm):
    tag_id = StringField(
        "tag_id", validators=[
            DataRequired(
                "You need to provide the tag_id that you want to add to the "
                "word"
            ),
        ]
    )
    description = StringField(
        "Description", validators=[
            DataRequired(
                "You need to provide the name of the tag you want to create"),
        ]
    )
