from datetime import datetime

from app import db_manager as db

from app.v1.database.models.base import model_dict


class Word(db.Model):
    __tablename__ = "word"
    __table_args__ = (
        db.UniqueConstraint("word", name="unq_word_indx"),
    )
    word_id = db.Column("id", db.String(50), primary_key=True)
    word = db.Column(db.String(400), nullable=False, index=True)
    length = db.Column(db.Integer(), nullable=False, index=True, default=0)
    date_created = db.Column(
        db.DateTime(), index=True, nullable=False, default=datetime.utcnow)
    ver_id = db.Column(db.Integer(), nullable=False, default=0)
    __mapper_args__ = {"version_id_col": ver_id}

    COLUMNS = ('word_id', 'word', 'length', 'date_created', 'ver')


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
