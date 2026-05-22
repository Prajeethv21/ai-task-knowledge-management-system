"""initial migration

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-22
"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

from app.database.base import Base


def upgrade():
    bind = op.get_bind()
    Base.metadata.create_all(bind=bind)


def downgrade():
    bind = op.get_bind()
    Base.metadata.drop_all(bind=bind)
