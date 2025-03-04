"""remove_test_schedule_id_column_from_reservations

Revision ID: 706ffc794c43
Revises: e6aab7191b1f
Create Date: 2025-03-03 07:27:10.788374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '706ffc794c43'
down_revision: Union[str, None] = 'e6aab7191b1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('reservations_test_schedule_id_fkey', 'reservations', type_='foreignkey')
    op.drop_column('reservations', 'test_schedule_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reservations', sa.Column('test_schedule_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('reservations_test_schedule_id_fkey', 'reservations', 'test_schedules', ['test_schedule_id'], ['id'])
    # ### end Alembic commands ###
