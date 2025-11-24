"""add selling_price and discount_price to products table

Revision ID: c8cd3196df6d
Revises: 6726748c6712
Create Date: 2025-07-30 02:35:20.266799

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c8cd3196df6d'
down_revision: Union[str, Sequence[str], None] = '6726748c6712'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
