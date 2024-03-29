"""added column for versioning models

Revision ID: 4aa65d5dad1c
Revises: ba3a93aaa857
Create Date: 2023-11-12 23:30:29.507193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aa65d5dad1c'
down_revision = 'ba3a93aaa857'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ver_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ver_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('word_tag', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ver_id', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('word_tag', schema=None) as batch_op:
        batch_op.drop_column('ver_id')

    with op.batch_alter_table('word', schema=None) as batch_op:
        batch_op.drop_column('ver_id')

    with op.batch_alter_table('tag', schema=None) as batch_op:
        batch_op.drop_column('ver_id')

    # ### end Alembic commands ###
