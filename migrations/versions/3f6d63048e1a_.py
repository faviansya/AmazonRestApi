"""empty message

Revision ID: 3f6d63048e1a
Revises: ed2fd7ac0ce7
Create Date: 2019-03-25 13:00:53.202853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f6d63048e1a'
down_revision = 'ed2fd7ac0ce7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transaction', sa.Column('item_gambar', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('item_harga', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('item_name', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('owner_alamat', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('owner_gambar', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('owner_name', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('user_alamat', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('user_gambar', sa.String(length=500), nullable=True))
    op.add_column('transaction', sa.Column('user_name', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction', 'user_name')
    op.drop_column('transaction', 'user_gambar')
    op.drop_column('transaction', 'user_alamat')
    op.drop_column('transaction', 'owner_name')
    op.drop_column('transaction', 'owner_gambar')
    op.drop_column('transaction', 'owner_alamat')
    op.drop_column('transaction', 'item_name')
    op.drop_column('transaction', 'item_harga')
    op.drop_column('transaction', 'item_gambar')
    # ### end Alembic commands ###
