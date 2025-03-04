"""change_test_schedule_time_unique

Revision ID: 14eb67026f3d
Revises: b1754b15e8ee
Create Date: 2025-03-03 02:33:40.949822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14eb67026f3d'
down_revision: Union[str, None] = 'b1754b15e8ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'test_schedules', ['time'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'test_schedules', type_='unique')
    # ### end Alembic commands ###
