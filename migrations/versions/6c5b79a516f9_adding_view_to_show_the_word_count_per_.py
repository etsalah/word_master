"""adding view to show the word count per tag

Revision ID: 6c5b79a516f9
Revises: 3e0668cb0321
Create Date: 2024-01-08 14:14:19.517972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c5b79a516f9'
down_revision = '3e0668cb0321'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
        CREATE OR REPLACE VIEW 
            vw_tag_word_count
        AS SELECT 
            t.id, t.tag, (
                SELECT
                    COUNT(id)
                FROM
                    word_tag wt
                WHERE
                    wt.tag_id = t.id
            ) AS word_count
        FROM
            tag AS t;
        """
    )


def downgrade():
    op.execute(
        """
        DROP VIEW vw_tag_word_count;
        """
    )
