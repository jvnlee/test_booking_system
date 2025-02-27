from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

# 중간 테이블 (Many-to-Many 관계)
reservation_test_schedule = Table(
    'reservation_test_schedules',
    Base.metadata,
    Column('reservation_id', Integer, ForeignKey('reservations.id', ondelete='CASCADE'), primary_key=True),
    Column('test_schedule_id', Integer, ForeignKey('test_schedules.id', ondelete='CASCADE'), primary_key=True)
)
