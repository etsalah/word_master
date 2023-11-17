"""make ver_id field not nullable on tag table

Revision ID: 061a586250cb
Revises: 4aa65d5dad1c
Create Date: 2023-11-15 21:26:13.368812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '061a586250cb'
down_revision = '4aa65d5dad1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.alter_column('ver_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.alter_column('ver_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###