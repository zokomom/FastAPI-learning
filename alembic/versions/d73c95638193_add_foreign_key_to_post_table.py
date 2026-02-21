"""add foreign-key to post table

Revision ID: d73c95638193
Revises: f1214ef07aae
Create Date: 2026-02-21 21:40:54.490398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd73c95638193'
down_revision: Union[str, Sequence[str], None] = 'f1214ef07aae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table='posts',referent_table='users',local_cols=['owner_id'],remote_cols=['user_id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk',table_name='posts')
    op.drop_column('posts',column_name='owner_id')
    pass
