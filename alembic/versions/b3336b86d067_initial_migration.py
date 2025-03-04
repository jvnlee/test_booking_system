"""Initial migration

Revision ID: b3336b86d067
Revises: 
Create Date: 2025-02-27 19:54:17.205579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3336b86d067'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('test_schedules',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('remaining_capacity', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('admin', 'company', name='roleenum', native_enum=False), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('test_schedule_id', sa.Integer(), nullable=False),
    sa.Column('participant_num', sa.Integer(), nullable=False),
    sa.Column('is_confirmed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['test_schedule_id'], ['test_schedules.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reservation_test_schedules',
    sa.Column('reservation_id', sa.Integer(), nullable=False),
    sa.Column('test_schedule_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['reservation_id'], ['reservations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['test_schedule_id'], ['test_schedules.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('reservation_id', 'test_schedule_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservation_test_schedules')
    op.drop_table('reservations')
    op.drop_table('users')
    op.drop_table('test_schedules')
    # ### end Alembic commands ###
