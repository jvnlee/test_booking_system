from datetime import time, date
from typing import List
from pydantic import BaseModel, Field
from app.model.reservation import ReservationStatus


class CreateReservationRequest(BaseModel):
    desired_date: date = Field(..., alias="desiredDate", examples=["2025-03-31"])
    start_time: time = Field(..., alias="startTime", examples=["14:00:00"])
    end_time: time = Field(..., alias="endTime", examples=["16:00:00"])
    participant_num: int = Field(..., alias="participantNum", examples=["20000"])


class ReservationItem(BaseModel):
    id: int
    reserved_user_name: str = Field(..., alias="reservedUserName", examples=["grepp"])
    reserved_date: date = Field(..., alias="reservedDate", examples=["2025-03-31"])
    reserved_times: List[time] = Field(..., alias="reservedTimes", examples=["14:00:00", "15:00:00"])
    reserved_participant_num: int = Field(..., alias="reservedParticipantNum", examples=["20000"])
    reservation_status: ReservationStatus

    class Config:
        populate_by_name = True
        by_alias = True


class ReadReservationsResponse(BaseModel):
    reservations: List[ReservationItem]
    total_count: int = Field(..., alias="totalCount")

    class Config:
        populate_by_name = True
        by_alias = True


class UpdateReservationRequest(BaseModel):
    desired_date: date = Field(..., alias="desiredDate", examples=["2025-03-31"])
    start_time: time = Field(..., alias="startTime", examples=["14:00:00"])
    end_time: time = Field(..., alias="endTime", examples=["16:00:00"])
    participant_num: int = Field(..., alias="participantNum", examples=["20000"])


class UpdateReservationStatusResponse(BaseModel):
    reservation_status: ReservationStatus = Field(..., alias="reservationStatus", examples=["CONFIRMED", "CANCELLED"])

    class Config:
        populate_by_name = True
        by_alias = True
