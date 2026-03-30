"""change blog content column from string to jsonb.

Revision ID: 3eec2712dfcf
Revises: 562317ab3c3f
Create Date: 2026-03-30 00:00:00.000000

"""
from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision: str = '3eec2712dfcf'
down_revision: Union[str, Sequence[str], None] = '562317ab3c3f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: convert content from VARCHAR to JSONB.

    Existing text content is wrapped in a BlockNote paragraph block structure
    so it remains valid after the type change.
    """
    # Step 1: Add a temporary JSONB column
    op.add_column('blogs', sa.Column('content_jsonb', JSONB, nullable=True))

    # Step 2: Migrate existing data — wrap plain text into BlockNote block format
    connection = op.get_bind()
    blogs_table = sa.table(
        'blogs',
        sa.column('id', sa.String),
        sa.column('content', sa.String),
        sa.column('content_jsonb', JSONB),
    )
    rows = connection.execute(sa.select(blogs_table.c.id, blogs_table.c.content)).fetchall()
    for row in rows:
        block_id = str(uuid.uuid4())
        blocknote_content = [{
            "id": block_id,
            "type": "paragraph",
            "props": {
                "textColor": "default",
                "backgroundColor": "default",
                "textAlignment": "left",
            },
            "content": [{"type": "text", "text": row.content, "styles": {}}],
            "children": [],
        }]
        connection.execute(
            blogs_table.update()
            .where(blogs_table.c.id == row.id)
            .values(content_jsonb=blocknote_content)
        )

    # Step 3: Drop old column and rename new one
    op.drop_column('blogs', 'content')
    op.alter_column('blogs', 'content_jsonb', new_column_name='content', nullable=False)


def downgrade() -> None:
    """Downgrade schema: convert content from JSONB back to VARCHAR.

    Extracts the plain text from the first text node of the first block.
    Falls back to an empty string if the structure is unexpected.
    """
    # Step 1: Add a temporary VARCHAR column
    op.add_column('blogs', sa.Column('content_text', sa.String, nullable=True))

    # Step 2: Migrate data back — extract text from BlockNote JSON
    connection = op.get_bind()
    blogs_table = sa.table(
        'blogs',
        sa.column('id', sa.String),
        sa.column('content', JSONB),
        sa.column('content_text', sa.String),
    )
    rows = connection.execute(sa.select(blogs_table.c.id, blogs_table.c.content)).fetchall()
    for row in rows:
        # Extract all text from all blocks
        text_parts = []
        if isinstance(row.content, list):
            for block in row.content:
                block_content = block.get("content", []) if isinstance(block, dict) else []
                for node in block_content:
                    if isinstance(node, dict) and node.get("type") == "text":
                        text_parts.append(node.get("text", ""))
        plain_text = "\n".join(text_parts) if text_parts else ""
        connection.execute(
            blogs_table.update()
            .where(blogs_table.c.id == row.id)
            .values(content_text=plain_text)
        )

    # Step 3: Drop old column and rename new one
    op.drop_column('blogs', 'content')
    op.alter_column('blogs', 'content_text', new_column_name='content', nullable=False)
