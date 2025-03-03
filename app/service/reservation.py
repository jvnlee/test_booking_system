from datetime import datetime, timedelta, date, time
from sqlalchemy.orm import Session
from app.model import Reservation, TestSchedule
from app.service.exception.not_enough_participant_capacity_exception import NotEnoughParticipantCapacityException
from app.service.exception.reservation_deadline_exceeded_exception import ReservationDeadlineExceededException
from app.service.exception.test_schedule_not_found_exception import TestScheduleNotFoundException


def create_reservation(
        db: Session,
        user_id: int,
        desired_date: date,
        start_time: time,
        end_time: time,
        participant_num: int
) -> Reservation:
    today = date.today()

    if desired_date - today < timedelta(days=3):
        raise ReservationDeadlineExceededException()

    start_datetime = datetime.combine(desired_date, start_time)
    end_datetime = datetime.combine(desired_date, end_time)

    test_schedules = db.query(TestSchedule).filter(
        TestSchedule.date_time >= start_datetime,
        TestSchedule.date_time < end_datetime
    ).all()

    if not test_schedules:
        raise TestScheduleNotFoundException()

    for schedule in test_schedules:
        if schedule.remaining_capacity < participant_num:
            raise NotEnoughParticipantCapacityException()

    new_reservation = Reservation(
        user_id=user_id,
        participant_num=participant_num
    )

    new_reservation.test_schedules = test_schedules

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation
