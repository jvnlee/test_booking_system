from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field


class TestScheduleItem(BaseModel):
    time: datetime = Field(..., examples=["2025-03-01T14:00:00"])
    remaining_capacity: int = Field(..., examples=[50000])


class ReadAvailableTestSchedulesResponse(BaseModel):
    schedules: List[TestScheduleItem]
