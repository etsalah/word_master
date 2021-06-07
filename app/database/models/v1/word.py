from datetime import datetime

from flask_sqlalchemy import model
from app import db_manager as db

from app.database.models.v1.base import model_dict


class Word(db.Model):
    __table_name__ = "word"
    id = db.Column(db.String(50), primary_key=True)
    word = db.Column(db.String(400), nullable=False, index=True)
    length = db.Column(db.Integer(), nullable=False, index=True, default=0)
    date_created = db.Column(
        db.DateTime(), index=True, nullable=False, default=datetime.utcnow)

    COLUMNS = ('id', 'word', 'length', 'date_created')


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
