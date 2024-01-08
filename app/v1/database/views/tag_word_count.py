
from app import db_manager as db

from app.v1.database.models.base import model_dict


class VwTagWordCount(db.Model):
    __tablename__ = "vw_tag_word_count"
    tag_id = db.Column("id", db.String(50), primary_key=True)
    tag = db.Column("tag", db.String(50))
    word_count = db.Column("word_count", db.Integer())

    COLUMNS = ('tag_id', 'tag', 'word_count', )


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
