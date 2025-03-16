"""Add user.patronomic with conflict

Revision ID: 8c7e8fab2664
Revises: d7120be63a33
Create Date: 2025-03-16 19:26:29.500223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8c7e8fab2664'
down_revision: Union[str, None] = 'a121127d3e17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("user", sa.Column("patronomic", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
