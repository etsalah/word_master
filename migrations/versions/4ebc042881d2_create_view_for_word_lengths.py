"""create view for word lengths

Revision ID: 4ebc042881d2
Revises: e6570740bdae
Create Date: 2023-11-16 09:53:39.592009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ebc042881d2'
down_revision = 'e6570740bdae'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            CREATE OR REPLACE VIEW
                vw_word_length_group
            AS SELECT
                w.length AS word_length,
                count(w.length) AS word_count
            FROM
                word w
            GROUP by
                w.length; 
        """
    )


def downgrade():
    op.execute("DROP VIEW vw_word_length_group;")
