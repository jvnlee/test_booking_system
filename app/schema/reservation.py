from datetime import time, date
from typing import List
from pydantic import BaseModel, Field
from app.model.reservation import ReservationStatus


class CreateReservationRequest(BaseModel):
    desired_date: date = Field(..., alias="desiredDate", examples=["2025-03-31"])
    start_time: time = Field(..., alias="startTime", examples=["14:00:00"])
    end_time: time = Field(..., alias="endTime", examples=["16:00:00"])
    participant_num: int = Field(..., alias="participantNum", examples=["20000"])


class CreateReservationResponse(BaseModel):
    id: int
    reserved_date: date = Field(..., alias="reservedDate", examples=["2025-03-31"])
    reserved_times: List[time] = Field(..., alias="reservedTimes", examples=["14:00:00", "15:00:00", "16:00:00"])
    reserved_participant_num: int = Field(..., alias="reservedParticipantNum", examples=["20000"])
    reservation_status: ReservationStatus

    class Config:
        populate_by_name = True
        by_alias = True
