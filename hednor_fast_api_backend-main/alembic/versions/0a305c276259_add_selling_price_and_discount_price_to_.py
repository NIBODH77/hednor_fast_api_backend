"""add selling_price and discount_price to products table

Revision ID: 0a305c276259
Revises: 2f712a856961
Create Date: 2025-07-30 02:47:39.890863

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a305c276259'
down_revision: Union[str, Sequence[str], None] = '2f712a856961'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
