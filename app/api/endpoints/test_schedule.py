from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.model import User
from app.schema.test_schedule import ReadAvailableTestSchedulesResponse, TestScheduleItem
from app.service.test_schedule import read_available_test_schedules


router = APIRouter()


@router.get("/", response_model=ReadAvailableTestSchedulesResponse, status_code=200)
def read_available_test_schedules_endpoint(
        desired_date: date = Query(
            ...,
            alias="desired-date",
            example="2025-03-01",
            description="Desired date in YYYY-MM-DD format"
        ),
        db: Session = Depends(get_db),
        _: User = Depends(get_current_user)
):
    available_test_schedules = read_available_test_schedules(
        db,
        desired_date
    )

    test_schedule_items = [
        TestScheduleItem(
            date_time=schedule.date_time,
            remaining_capacity=schedule.remaining_capacity
        ) for schedule in available_test_schedules
    ]

    return ReadAvailableTestSchedulesResponse(
        schedules=[test_schedule_items]
    )
