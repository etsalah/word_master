from datetime import datetime

from app import db_manager as db

from app.v1.database.models.base import model_dict


class VwWordLengthGroup(db.Model):
    __tablename__ = "vw_word_length_group"
    word_length = db.Column("word_length", db.Integer(), primary_key=True)
    word_count = db.Column("word_count", db.Integer())

    COLUMNS = ('word_length', 'word_count', )


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
