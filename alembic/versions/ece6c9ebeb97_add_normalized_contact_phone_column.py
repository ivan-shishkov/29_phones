"""add normalized contact phone column

Revision ID: ece6c9ebeb97
Revises: 
Create Date: 2018-12-09 21:46:17.286164

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ece6c9ebeb97'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'orders',
        sa.Column('contact_phone_normalized', sa.String(100), index=True),
    )


def downgrade():
    op.drop_column('orders', 'contact_phone_normalized')
