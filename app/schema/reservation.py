from datetime import time, date
from typing import List
from pydantic import BaseModel, Field
from app.model.reservation import ReservationStatus


class CreateReservationRequest(BaseModel):
    desired_date: date = Field(
        ...,
        alias="desiredDate",
        examples=["2025-03-31"],
        description="예약할 시험 날짜"
    )
    start_time: time = Field(
        ...,
        alias="startTime",
        examples=["14:00:00"],
        description="시험 시작 시간"
    )
    end_time: time = Field(
        ...,
        alias="endTime",
        examples=["16:00:00"],
        description="시험 종료 시간"
    )
    participant_num: int = Field(
        ...,
        alias="participantNum",
        examples=["20000"],
        description="시험 응시 인원"
    )


class ReservationItem(BaseModel):
    id: int = Field(
        ...,
        examples=["1"],
        description="예약 번호"
    )
    reserved_user_name: str = Field(
        ...,
        alias="reservedUserName",
        examples=["grepp"],
        description="예약한 사용자의 이름 (기업 고객의 경우 회사명)"
    )
    reserved_date: date = Field(
        ...,
        alias="reservedDate",
        examples=["2025-03-31"],
        description="예약된 시험 날짜"
    )
    reserved_times: List[time] = Field(
        ...,
        alias="reservedTimes",
        examples=["14:00:00", "15:00:00"],
        description="예약된 시험 시간대 목록 (예시는 14:00:00 ~ 14:59:59와 15:00:00 ~ 15:59:59 총 2개의 시간대를 나타냄"
    )
    reserved_participant_num: int = Field(
        ...,
        alias="reservedParticipantNum",
        examples=["20000"],
        description="예약된 응시 인원수"
    )
    reservation_status: ReservationStatus = Field(
        ...,
        alias="reservationStatus",
        examples=["REQUESTED"],
        description="예약 상태"
    )

    class Config:
        populate_by_name = True
        by_alias = True


class ReadReservationsResponse(BaseModel):
    reservations: List[ReservationItem]
    total_count: int = Field(
        ...,
        alias="totalCount",
        examples=["1"],
        description="조회된 예약 내역의 총 개수"
    )

    class Config:
        populate_by_name = True
        by_alias = True


class UpdateReservationRequest(BaseModel):
    desired_date: date = Field(
        ...,
        alias="desiredDate",
        examples=["2025-03-31"],
        description="예약할 시험 날짜"
    )
    start_time: time = Field(
        ...,
        alias="startTime",
        examples=["14:00:00"],
        description="시험 시작 시간"
    )
    end_time: time = Field(
        ...,
        alias="endTime",
        examples=["16:00:00"],
        description="시험 종료 시간"
    )
    participant_num: int = Field(
        ...,
        alias="participantNum",
        examples=["20000"],
        description="시험 응시 인원"
    )


class UpdateReservationStatusResponse(BaseModel):
    reservation_status: ReservationStatus = Field(
        ...,
        alias="reservationStatus",
        examples=["CONFIRMED", "CANCELLED"],
        description="예약 상태"
    )

    class Config:
        populate_by_name = True
        by_alias = True
