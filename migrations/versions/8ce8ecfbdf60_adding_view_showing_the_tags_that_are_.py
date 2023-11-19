"""adding view showing the tags that are attached to words

Revision ID: 8ce8ecfbdf60
Revises: d179e1961def
Create Date: 2023-11-18 20:28:55.036030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce8ecfbdf60'
down_revision = 'd179e1961def'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
    """
        CREATE OR REPLACE VIEW
            vw_word_tag_list
        AS SELECT
            word_tag.id AS word_tag_id,
            word_tag.word_id AS word_id,
            word_tag.tag_id AS tag_id,
            tag.tag AS tag,
            word_tag.description AS description 
        FROM
            word_tag
        JOIN
            tag
        ON
            tag.id = word_tag.tag_id;
    """
    )


def downgrade():
    op.execute(
    """
        DROP VIEW vw_word_tag_list;
    """
    )
