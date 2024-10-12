"""Auto-generated migration

Revision ID: c07c162ec21d
Revises: 8cd403036cca
Create Date: 2024-10-12 22:26:05.655275+03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import pgvector

# revision identifiers, used by Alembic.
revision: str = 'c07c162ec21d'
down_revision: Union[str, None] = '8cd403036cca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('tags_user_group_id_fkey', 'tags', type_='foreignkey')
    op.drop_column('tags', 'user_group_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('user_group_id', sa.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('tags_user_group_id_fkey', 'tags', 'user_groups', ['user_group_id'], ['id'])
    # ### end Alembic commands ###
