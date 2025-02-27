from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.model.reservation_test_schedule import reservation_test_schedule


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    test_schedule_id = Column(Integer, ForeignKey('test_schedules.id'), nullable=False)
    participant_num = Column(Integer, nullable=False)  # 시험 응시 인원
    is_confirmed = Column(Boolean, nullable=False, default=False)  # 예약 확정 여부

    user = relationship("User", back_populates='reservations')
    test_schedules = relationship(
        'TestSchedule',
        secondary=reservation_test_schedule,
        back_populates='reservations'
    )
