"""add vw_tags_word_list to the database to represent view that show list of word attached to a particular tag

Revision ID: 3e0668cb0321
Revises: 8ce8ecfbdf60
Create Date: 2023-11-28 16:41:14.880733

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e0668cb0321'
down_revision = '8ce8ecfbdf60'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
    """
        CREATE OR REPLACE VIEW
            vw_tags_word_list
        AS SELECT
            wt.id AS word_tag_id,
            w.id AS word_id,
            w.word AS word,
            t.id AS tag_id,
            t.tag AS tag,
            wt.description AS description
        FROM 
            word w 
        JOIN
            word_tag wt 
        ON
            w.id = wt.word_id 
        JOIN 
            tag t 
        ON
            t.id = wt.tag_id;
    """
    )


def downgrade():
    op.execute("""DROP VIEW vw_tags_word_list;""")
