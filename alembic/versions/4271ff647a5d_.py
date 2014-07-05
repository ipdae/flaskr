"""empty message

Revision ID: 4271ff647a5d
Revises: 1e4dbd908e8d
Create Date: 2014-07-04 17:06:01.981123

"""

# revision identifiers, used by Alembic.
revision = '4271ff647a5d'
down_revision = '1e4dbd908e8d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(
        "insert into facebooklogins (email) values ('qooraven@gmail.com')")


def downgrade():
    op.execute(
        "delete from facebooklogins")
