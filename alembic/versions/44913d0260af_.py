"""empty message

Revision ID: 44913d0260af
Revises: f3d8173d642
Create Date: 2014-05-10 14:44:45.395071

"""

# revision identifiers, used by Alembic.
revision = '44913d0260af'
down_revision = 'f3d8173d642'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('entries', sa.Column('etc', sa.String(length=255), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('entries', 'etc')
    ### end Alembic commands ###
