"""Auto-generated migration

Revision ID: 0b0542d427f5
Revises: a1a47ed8857a
Create Date: 2024-10-14 00:16:46.080102+03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import pgvector

# revision identifiers, used by Alembic.
revision: str = '0b0542d427f5'
down_revision: Union[str, None] = 'a1a47ed8857a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('content_hash', sa.String(length=64), nullable=False))
    op.create_unique_constraint(None, 'documents', ['content_hash'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='unique')
    op.drop_column('documents', 'content_hash')
    # ### end Alembic commands ###
