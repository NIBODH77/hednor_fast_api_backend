"""add selling_price and discount_price to products table 2

Revision ID: 6726748c6712
Revises: f93a122aa3ca
Create Date: 2025-07-30 02:21:57.402590

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6726748c6712'
down_revision: Union[str, Sequence[str], None] = 'f93a122aa3ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
