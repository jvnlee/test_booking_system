from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class TestScheduleItem(BaseModel):
    date_time: datetime = Field(
        ...,
        alias="dateTime",
        examples=["2025-03-01T14:00:00"],
        description="시험 날짜와 시간"
    )
    remaining_capacity: int = Field(
        ...,
        alias="remainingCapacity",
        examples=[50000],
        description="잔여 수용 인원"
    )

    class Config:
        populate_by_name = True
        by_alias = True


class ReadAvailableTestSchedulesResponse(BaseModel):
    schedules: List[TestScheduleItem]
