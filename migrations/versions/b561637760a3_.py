"""empty message

Revision ID: b561637760a3
Revises: 0b3ebefb936a
Create Date: 2019-03-23 16:53:35.133342

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b561637760a3'
down_revision = '0b3ebefb936a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('qty', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'qty')
    # ### end Alembic commands ###
