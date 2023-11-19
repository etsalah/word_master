from datetime import datetime

from app import db_manager as db

from app.v1.database.models.base import model_dict


class VwWordTagList(db.Model):
    __tablename__ = "vw_word_tag_list"
    word_tag_id = db.Column("word_tag_id", db.String(50), primary_key=True)
    word_id = db.Column("word_id", db.String(50), primary_key=True)
    tag_id = db.Column("tag_id", db.String(50), primary_key=True)
    tag = db.Column("tag", db.String(400))
    description = db.Column("description", db.UnicodeText())

    COLUMNS = ('word_tag_id', 'word_id', 'tag_id', 'tag', 'description', )


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
