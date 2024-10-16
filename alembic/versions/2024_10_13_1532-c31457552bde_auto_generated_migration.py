"""Auto-generated migration

Revision ID: c31457552bde
Revises: 1c613cc00f31
Create Date: 2024-10-13 15:32:04.423939+03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import pgvector

# revision identifiers, used by Alembic.
revision: str = 'c31457552bde'
down_revision: Union[str, None] = '1c613cc00f31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('documents', sa.Column('start_date', sa.TIMESTAMP(timezone=True), nullable=False))
    op.add_column('documents', sa.Column('end_date', sa.TIMESTAMP(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('documents', 'end_date')
    op.drop_column('documents', 'start_date')
    # ### end Alembic commands ###
