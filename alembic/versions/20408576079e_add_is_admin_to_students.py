
"""add is_admin to students

Revision ID: 20408576079e
Revises: 734561ab3d28
Create Date: 2026-09-26 12:09:42.125252

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20408576079e"
down_revision: Union[str, Sequence[str], None] = "734561ab3d28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "students",
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("students", "is_admin")

