"""empty message

Revision ID: 131b57b8ee7f
Revises: 43a684ab9f79
Create Date: 2014-05-17 14:48:36.238485

"""

# revision identifiers, used by Alembic.
revision = '131b57b8ee7f'
down_revision = '43a684ab9f79'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(
        "insert into logins (username, password) values ('admin', 'default')") 


def downgrade():
    op.execute(
        "delete from logins") 
