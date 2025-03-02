import enum
from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.model.reservation_test_schedule import reservation_test_schedule


class ReservationStatus(str, enum.Enum):
    REQUESTED = 'requested'
    CONFIRMED = 'confirmed'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'


class Reservation(Base):
    __tablename__ = 'reservations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    test_schedule_id = Column(Integer, ForeignKey('test_schedules.id'), nullable=False)
    participant_num = Column(Integer, nullable=False)  # 시험 응시 인원
    status = Column(Enum(ReservationStatus, native_enum=False), nullable=False, default=ReservationStatus.REQUESTED.value)  # 예약 확정 여부

    user = relationship("User", back_populates='reservations')
    test_schedules = relationship(
        'TestSchedule',
        secondary=reservation_test_schedule,
        back_populates='reservations'
    )
