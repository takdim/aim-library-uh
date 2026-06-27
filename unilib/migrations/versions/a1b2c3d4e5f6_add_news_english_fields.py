"""add_news_english_fields

Revision ID: a1b2c3d4e5f6
Revises: 70c719428531
Create Date: 2026-06-28 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '70c719428531'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title_en', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('excerpt_en', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('content_en', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('news', schema=None) as batch_op:
        batch_op.drop_column('content_en')
        batch_op.drop_column('excerpt_en')
        batch_op.drop_column('title_en')
