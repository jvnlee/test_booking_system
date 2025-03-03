from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, is_admin_user
from app.model import User
from app.schema.reservation import ReservationItem, CreateReservationRequest, ReadReservationsResponse, \
    UpdateReservationRequest, UpdateReservationStatusResponse
from app.service.reservation import create_reservation, read_all_reservations, update_reservation, \
    cancel_reservation, confirm_reservation

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
        reserved_user_name=new_reservation.user.name,
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
    reservations, total_count = read_all_reservations(
        db,
        limit,
        offset,
        user
    )

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


@router.put("/{reservation_id}", response_model=ReservationItem, status_code=200)
def update_reservation_endpoint(
        reservation_id: int,
        request: UpdateReservationRequest,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    updated_reservation = update_reservation(
        db,
        user,
        reservation_id,
        request.desired_date,
        request.start_time,
        request.end_time,
        request.participant_num,
    )

    reserved_times = [
        schedule.date_time.time() for schedule in updated_reservation.test_schedules
    ]

    return ReservationItem(
        id=updated_reservation.id,
        reserved_user_name=updated_reservation.user.name,
        reserved_date=request.desired_date,
        reserved_times=reserved_times,
        reserved_participant_num=request.participant_num,
        reservation_status=updated_reservation.status
    )


@router.patch("/{reservation_id}/confirm", status_code=200)
def confirm_reservation_endpoint(
        reservation_id: int,
        db: Session = Depends(get_db),
        _: User = Depends(is_admin_user)
):
    confirmed_status = confirm_reservation(
        db,
        reservation_id,
    )

    return UpdateReservationStatusResponse(
        reservation_status=confirmed_status
    )


@router.patch("/{reservation_id}/cancel", status_code=200)
def cancel_reservation_endpoint(
        reservation_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    cancelled_status = cancel_reservation(
        db,
        user,
        reservation_id,
    )

    return UpdateReservationStatusResponse(
        reservation_status=cancelled_status
    )
