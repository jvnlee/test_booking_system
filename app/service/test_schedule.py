from datetime import datetime, date
from sqlalchemy import Date, cast
from sqlalchemy.orm import Session
from app.model import TestSchedule


def read_available_test_schedules(db: Session, desired_date: date):
    return db.query(TestSchedule).filter(
        TestSchedule.remaining_capacity > 0,
        cast(TestSchedule.time, Date) == desired_date
    ).all()
