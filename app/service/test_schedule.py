from datetime import datetime, date
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session

from app.exception.test_schedule_not_found_exception import TestScheduleNotFoundException
from app.model import TestSchedule


def read_available_test_schedules(db: Session, desired_date: date):
    test_schedules = db.query(TestSchedule).filter(
        TestSchedule.remaining_capacity > 0,
        cast(TestSchedule.date_time, Date) == desired_date
    ).all()

    if not test_schedules:
        raise TestScheduleNotFoundException()

    return test_schedules
