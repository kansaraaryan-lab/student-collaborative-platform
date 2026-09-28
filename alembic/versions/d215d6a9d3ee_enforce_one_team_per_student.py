"""enforce one team per student

Revision ID: d215d6a9d3ee
Revises: d1d5b5b2be02
Create Date: 2026-09-26 19:22:59.561645

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd215d6a9d3ee'
down_revision: Union[str, Sequence[str], None] = 'd1d5b5b2be02'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_unique_constraint(
        "uq_team_members_student_id",
        "team_members",
        ["student_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_team_members_student_id",
        "team_members",
        type_="unique",
    )