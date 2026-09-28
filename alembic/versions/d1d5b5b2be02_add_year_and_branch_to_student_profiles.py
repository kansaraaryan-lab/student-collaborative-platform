"""add year and branch to student profiles

Revision ID: d1d5b5b2be02
Revises: 2382998efa60
Create Date: 2026-09-26 17:36:57.099144

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd1d5b5b2be02'
down_revision: Union[str, Sequence[str], None] = '2382998efa60'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
   
    op.add_column('student_profiles', sa.Column('year', sa.String(length=50), nullable=True))
    op.add_column('student_profiles', sa.Column('branch', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_column('student_profiles', 'branch')
    op.drop_column('student_profiles', 'year')
    op.create_table('messages',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('sender_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('receiver_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['receiver_id'], ['students.id'], name=op.f('messages_receiver_id_fkey')),
    sa.ForeignKeyConstraint(['sender_id'], ['students.id'], name=op.f('messages_sender_id_fkey')),
    sa.PrimaryKeyConstraint('id', name=op.f('messages_pkey'))
    )
    # ### end Alembic commands ###
