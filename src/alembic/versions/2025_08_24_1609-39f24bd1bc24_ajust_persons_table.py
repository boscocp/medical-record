"""ajust persons table

Revision ID: 39f24bd1bc24
Revises: db042c0f76d1
Create Date: 2025-08-24 16:09:53.372610

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "39f24bd1bc24"
down_revision: Union[str, Sequence[str], None] = "db042c0f76d1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
