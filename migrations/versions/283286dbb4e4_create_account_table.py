"""create account table

Revision ID: 283286dbb4e4
Revises: 4358f338d845
Create Date: 2025-06-10 17:25:28.219256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '283286dbb4e4'
down_revision: Union[str, None] = '4358f338d845'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
