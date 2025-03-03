from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.model import User
from app.schema.test_schedule import ReadAvailableTestSchedulesResponse, TestScheduleItem
from app.service.test_schedule import read_available_test_schedules


router = APIRouter()


@router.get(
    "/",
    response_model=ReadAvailableTestSchedulesResponse,
    status_code=200,
    summary="시험 일정 조회",
    description="""
    원하는 날짜에 대해 예약 신청 가능한 시험 일정 목록을 조회합니다.  
    <br>시험 일정은 1시간 단위로 이루어져있으며, 시작 시간 기준입니다. (14:00:00는 14:00:00부터 14:59:59까지의 1시간을 의미합니다)
    """
)
def read_available_test_schedules_endpoint(
        desired_date: date = Query(
            ...,
            alias="desired-date",
            example="2025-03-01",
            description="원하는 시험 날짜. YYYY-MM-DD 포맷"
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
        schedules=test_schedule_items
    )
