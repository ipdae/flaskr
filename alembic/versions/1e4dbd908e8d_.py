"""empty message

Revision ID: 1e4dbd908e8d
Revises: 149376522ed6
Create Date: 2014-07-04 16:58:16.534418

"""

# revision identifiers, used by Alembic.
revision = '1e4dbd908e8d'
down_revision = '131b57b8ee7f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('facebooklogins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('facebooklogins')
    ### end Alembic commands ###
