
from app import db_manager as db

from app.v1.database.models.base import model_dict


class VwTagWordList(db.Model):
    __tablename__ = "vw_tags_word_list"
    word_tag_id = db.Column("word_tag_id", db.String(50), primary_key=True)
    word_id = db.Column("word_id", db.String(50))
    word = db.Column("word", db.String(400))
    tag = db.Column("tag", db.String(400))
    tag_id = db.Column("tag_id", db.String(50), primary_key=True)
    description = db.Column("description", db.UnicodeText())

    COLUMNS = ('word_tag_id', 'word_id', 'tag_id', 'tag', 'description', 'word')


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
