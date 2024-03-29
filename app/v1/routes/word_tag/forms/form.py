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


class BulkForm(FlaskForm):
    choosen_words = StringField(
        "choosen_words", validators=[
            DataRequired(
                "You need to provide a list of choosen words that need to "
                "be tagged"
            ),
        ]
    )
    tag_id = StringField(
        "tag_id", validators=[
            DataRequired(
                "You need to provide the id of the tag you want to add to "
                "the words"
            ),
        ]
    )
    description = StringField(
        "description", validators=[
            DataRequired("Provide a description for the tag you are adding")
        ]
    )
