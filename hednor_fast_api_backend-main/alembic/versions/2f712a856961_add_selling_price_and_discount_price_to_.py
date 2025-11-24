"""add selling_price and discount_price to products table

Revision ID: 2f712a856961
Revises: c8cd3196df6d
Create Date: 2025-07-30 02:45:21.383424

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f712a856961'
down_revision: Union[str, Sequence[str], None] = 'c8cd3196df6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
