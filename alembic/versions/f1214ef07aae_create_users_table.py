"""create users table

Revision ID: f1214ef07aae
Revises: 631e5da4f022
Create Date: 2026-02-21 21:22:15.166047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1214ef07aae'
down_revision: Union[str, Sequence[str], None] = '631e5da4f022'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('user_id',sa.Integer(),primary_key=True,nullable=False),
    sa.Column('email',sa.String(),nullable=False,unique=True),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
