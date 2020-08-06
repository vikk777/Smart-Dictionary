"""empty message

Revision ID: be0d74508d11
Revises: e526f5536c8e
Create Date: 2020-04-22 20:01:23.689619

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'be0d74508d11'
down_revision = 'e526f5536c8e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dictionaries_ibfk_1', 'dictionaries', type_='foreignkey')
    op.drop_column('dictionaries', 'user_id')
    op.drop_constraint('mistakes_ibfk_2', 'mistakes', type_='foreignkey')
    op.drop_constraint('mistakes_ibfk_1', 'mistakes', type_='foreignkey')
    op.create_foreign_key(None, 'mistakes', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'mistakes', 'words', ['word_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('words_ibfk_1', 'words', type_='foreignkey')
    op.create_foreign_key(None, 'words', 'dictionaries', ['dictionary_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'words', type_='foreignkey')
    op.create_foreign_key('words_ibfk_1', 'words', 'dictionaries', ['dictionary_id'], ['id'])
    op.drop_constraint(None, 'mistakes', type_='foreignkey')
    op.drop_constraint(None, 'mistakes', type_='foreignkey')
    op.create_foreign_key('mistakes_ibfk_1', 'mistakes', 'users', ['user_id'], ['id'])
    op.create_foreign_key('mistakes_ibfk_2', 'mistakes', 'words', ['word_id'], ['id'])
    op.add_column('dictionaries', sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.create_foreign_key('dictionaries_ibfk_1', 'dictionaries', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###