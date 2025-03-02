from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.model.reservation_test_schedule import reservation_test_schedule


class TestSchedule(Base):
    __tablename__ = 'test_schedules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime, unique=True, nullable=False)  # 시험 일시
    remaining_capacity = Column(Integer, nullable=False, default=50000)  # 남은 수용 가능 인원

    reservations = relationship(
        'Reservation',
        secondary=reservation_test_schedule,
        back_populates='test_schedules'
    )
