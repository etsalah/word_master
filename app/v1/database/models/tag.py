from datetime import datetime

from app import db_manager as db

from app.v1.database.models.base import model_dict


class Tag(db.Model):
    __tablename__ = "tag"
    __table_args__ = (
        db.UniqueConstraint("tag", name="unq_tag_indx"),
    )

    tag_id = db.Column("id", db.String(50), primary_key=True)
    tag = db.Column(db.String(400), nullable=False, index=True)
    date_created = db.Column(
        db.DateTime(), index=True, nullable=False, default=datetime.utcnow)
    ver_id = db.Column(db.Integer(), nullable=True, default=0)

    __mapper_args__ = {"version_id_col": ver_id}

    COLUMNS = ('tag_id', 'tag', 'date_created', 'ver_id')


    def to_dict(self):
        return model_dict(self, self.COLUMNS)
