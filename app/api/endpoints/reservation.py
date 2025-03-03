from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.model import User
from app.schema.reservation import CreateReservationResponse, CreateReservationRequest
from app.service.reservation import create_reservation

router = APIRouter()


@router.post("/", response_model=CreateReservationResponse, status_code=201)
def create_reservation_endpoint(
        request: CreateReservationRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    new_reservation = create_reservation(
        db,
        user.id,
        request.desired_date,
        request.start_time,
        request.end_time,
        request.participant_num
    )

    reserved_times = [
        schedule.date_time.time() for schedule in new_reservation.test_schedules
    ]

    return CreateReservationResponse(
        id=new_reservation.id,
        reserved_date=request.desired_date,
        reserved_times=reserved_times,
        reserved_participant_num=request.participant_num,
        reservation_status=new_reservation.status
    )
