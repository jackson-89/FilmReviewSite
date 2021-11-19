"""added a description to course model

Revision ID: bd10b1769263
Revises: 34310442cb3d
Create Date: 2021-11-19 12:03:12.711105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd10b1769263'
down_revision = '34310442cb3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reviews', 'description')
    # ### end Alembic commands ###
