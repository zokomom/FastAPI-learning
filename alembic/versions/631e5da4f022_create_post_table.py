"""create post table

Revision ID: 631e5da4f022
Revises: 
Create Date: 2026-02-21 17:49:22.507450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '631e5da4f022'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
    sa.Column('title',sa.String(),nullable=False),
    sa.Column('content',sa.String(),nullable=False),
    sa.Column('published',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
