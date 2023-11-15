from datetime import datetime

from app import db_manager as db

from app.v1.database.models.base import model_dict


class WordTag(db.Model):
    __tablename__ = "word_tag"
    __table_args__ = (
        db.UniqueConstraint("tag_id", "word_id", name="unq_word_tag_indx"),
        db.ForeignKeyConstraint(
            ["tag_id", ], ["tag.id", ], name="fk_word_tag_tag_indx"),
        db.ForeignKeyConstraint(
            ["word_id", ], ["word.id", ], name="fk_word_tag_word_indx"),
    )
    word_tag_id = db.Column("id", db.String(50), primary_key=True)
    tag_id = db.Column(db.String(50), nullable=False, index=True)
    word_id = db.Column(db.String(50), nullable=False, index=True)
    ver_id = db.Column(db.Integer(), nullable=False, default=0)
    date_created = db.Column(
        db.DateTime(), index=True, nullable=False, default=datetime.utcnow)
    __mapper_args__ = {"version_id_col": ver_id}

    COLUMNS = ('word_tag_id', 'tag_id', 'word_id', 'date_created', 'ver_id')


    def to_dict(self):
        return model_dict(self, self.COLUMNS)