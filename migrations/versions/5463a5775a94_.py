"""empty message

Revision ID: 5463a5775a94
Revises: 4c7a7f704600
Create Date: 2020-04-16 19:54:22.113939

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5463a5775a94'
down_revision = '4c7a7f704600'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.add_column('users', sa.Column('username', sa.String(length=24), nullable=True))
    op.drop_column('users', 'name')
    op.drop_column('users', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password', mysql.VARCHAR(length=128), nullable=True))
    op.add_column('users', sa.Column('name', mysql.VARCHAR(length=24), nullable=True))
    op.drop_column('users', 'username')
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
