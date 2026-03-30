"""add blog status and published snapshot columns.

Revision ID: 7b61e071ad40
Revises: 3eec2712dfcf
Create Date: 2026-03-30 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '7b61e071ad40'
down_revision: Union[str, Sequence[str], None] = '3eec2712dfcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add status, published_title, published_content, and published_at columns to blogs."""
    op.add_column('blogs', sa.Column('status', sa.String(20), nullable=False, server_default='draft'))
    op.add_column('blogs', sa.Column('published_title', sa.String(100), nullable=True))
    op.add_column('blogs', sa.Column(
        'published_content',
        sa.JSON().with_variant(JSONB, 'postgresql'),
        nullable=True
    ))
    op.add_column('blogs', sa.Column('published_at', sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    """Remove status, published_title, published_content, and published_at columns from blogs."""
    op.drop_column('blogs', 'published_at')
    op.drop_column('blogs', 'published_content')
    op.drop_column('blogs', 'published_title')
    op.drop_column('blogs', 'status')
