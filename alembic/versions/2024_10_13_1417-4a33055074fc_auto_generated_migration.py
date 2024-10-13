"""Auto-generated migration

Revision ID: 4a33055074fc
Revises: 
Create Date: 2024-10-13 14:17:34.751855+03:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import pgvector

# revision identifiers, used by Alembic.
revision: str = '4a33055074fc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('notification_days_before_expiry', sa.Integer(), nullable=True))
    op.add_column('tags', sa.Column('notification_frequency', sa.Integer(), nullable=True))
    op.alter_column('tags', 'notify',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('false'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tags', 'notify',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('false'))
    op.drop_column('tags', 'notification_frequency')
    op.drop_column('tags', 'notification_days_before_expiry')
    # ### end Alembic commands ###
