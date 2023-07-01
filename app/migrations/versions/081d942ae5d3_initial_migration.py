"""initial migration

Revision ID: 081d942ae5d3
Revises: 
Create Date: 2023-07-01 09:30:51.342208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '081d942ae5d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('episodes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('rating', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('episodes')
    # ### end Alembic commands ###