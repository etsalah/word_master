from datetime import datetime

from app import db_manager as db

from app.v1.database.models.base import model_dict


class Tag(db.Model):
    __table_name__ = "tag"
    __table_args__ = (
        db.UniqueConstraint("tag", name="unq_tag_indx"),
    )
    id = db.Column(db.String(50), primary_key=True)
    tag = db.Column(db.String(400), nullable=False, index=True)
    date_created = db.Column(
        db.DateTime(), index=True, nullable=False, default=datetime.utcnow)

    COLUMNS = ('id', 'tag', 'date_created')


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
