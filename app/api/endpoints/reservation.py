from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.model import User
from app.model.user import UserRole
from app.schema.reservation import ReservationItem, CreateReservationRequest, ReadReservationsResponse
from app.service.reservation import create_reservation, read_all_reservations

router = APIRouter()


@router.post("/", response_model=ReservationItem, status_code=201)
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

    return ReservationItem(
        id=new_reservation.id,
        reserved_date=request.desired_date,
        reserved_times=reserved_times,
        reserved_participant_num=request.participant_num,
        reservation_status=new_reservation.status
    )


@router.get("/", response_model=ReadReservationsResponse, status_code=200)
def read_all_reservations_endpoint(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0)
):
    if user.role == UserRole.ADMIN:
        reservations, total_count = read_all_reservations(db, limit, offset, user_id=None, is_admin=True)
    else:
        reservations, total_count = read_all_reservations(db, limit, offset, user_id=user.id, is_admin=False)

    reservation_items = [
        ReservationItem(
            id=reservation.id,
            reserved_user_name=reservation.user.name,
            reserved_date=reservation.test_schedules[0].date_time.date(),
            reserved_times=[
                schedule.date_time.time()
                for schedule in reservation.test_schedules
            ],
            reserved_participant_num=reservation.participant_num,
            reservation_status=reservation.status
        ) for reservation in reservations
    ]

    return ReadReservationsResponse(
        reservations=reservation_items,
        total_count=total_count
    )
