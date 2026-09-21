"""update rooms with division

Revision ID: 289f7c110c05
Revises: 53439514035b
Create Date: 2026-09-02 05:05:55.498247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '289f7c110c05'
down_revision: Union[str, Sequence[str], None] = '53439514035b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add division temporarily as nullable
    op.add_column(
        "rooms",
        sa.Column("division", sa.String(length=10), nullable=True),
    )

    # Give existing rooms a division
    op.execute(
        "UPDATE rooms SET division = 'A' WHERE division IS NULL"
    )

    # Make division required
    op.alter_column(
        "rooms",
        "division",
        existing_type=sa.String(length=10),
        nullable=False,
    )

    # Make branch optional and increase its length
    op.alter_column(
        "rooms",
        "branch",
        existing_type=sa.VARCHAR(length=50),
        type_=sa.String(length=100),
        nullable=True,
    )

    # Replace the old uniqueness rule
    op.drop_constraint(
        op.f("uq_room_year_branch"),
        "rooms",
        type_="unique",
    )

    op.create_unique_constraint(
        "uq_room_year_branch_division",
        "rooms",
        ["year", "branch", "division"],
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        "uq_room_year_branch_division",
        "rooms",
        type_="unique",
    )

    op.create_unique_constraint(
        op.f("uq_room_year_branch"),
        "rooms",
        ["year", "branch"],
    )

    op.alter_column(
        "rooms",
        "branch",
        existing_type=sa.String(length=100),
        type_=sa.VARCHAR(length=50),
        nullable=True,
    )

    op.drop_column("rooms", "division")
    # ### end Alembic commands ###
