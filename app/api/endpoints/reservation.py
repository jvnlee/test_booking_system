from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user, is_admin_user
from app.model import User
from app.schema.reservation import ReservationItem, CreateReservationRequest, ReadReservationsResponse, \
    UpdateReservationRequest, UpdateReservationStatusResponse
from app.service.reservation import create_reservation, read_all_reservations, update_reservation, \
    cancel_reservation, confirm_reservation

router = APIRouter()


@router.post(
    "/",
    response_model=ReservationItem,
    status_code=201,
    summary="예약 신청",
    description="""
    예약은 시험 시작 3일 전까지 신청 가능합니다.  
    <br>또한, 각 시간대의 잔여 수용 인원만큼만 신청 가능합니다. (동 시간대 최대 수용 인원: 5만명)
    """,
    responses={
        201: {"description": "예약 신청 성공"},
        400: {"description": "신청 불가능한 날짜이거나, 수용 가능 인원을 초과한 경우"},
        401: {"description": "Authorization 헤더를 통한 JWT 인증이 되지 않은 경우"},
        404: {"description": "신청하려는 날짜와 시간에 대한 시험 일정이 존재하지 않는 경우"}
    }
)
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


@router.get(
    "/",
    response_model=ReadReservationsResponse,
    status_code=200,
    summary="예약 조회",
    description="""
    기업 고객(COMPANY): 본인이 신청한 예약만 조회 가능합니다.  
    <br>관리자(ADMIN): 모든 예약을 조회할 수 있습니다.
    """,
    responses={
        200: {"description": "예약 조회 성공"},
        401: {"description": "Authorization 헤더를 통한 JWT 인증이 되지 않은 경우"}
    }
)
def read_all_reservations_endpoint(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user),
        limit: int = Query(10, ge=1, le=100, description="페이지 당 표시할 예약 개수"),
        offset: int = Query(0, ge=0, description="페이지 번호")
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


@router.put(
    "/{reservation_id}",
    response_model=ReservationItem,
    status_code=200,
    summary="예약 수정",
    description="""
    기업 고객(COMPANY): 본인이 신청한 예약만 수정 가능합니다. 단, 예약 확정 전에만 수정이 가능합니다.  
    <br>관리자(ADMIN): 모든 예약을 수정할 수 있습니다.
    """,
    responses={
        200: {"description": "예약 수정 성공"},
        400: {"description": "신청 불가능한 날짜이거나, 수용 가능 인원을 초과한 경우"},
        401: {"description": "Authorization 헤더를 통한 JWT 인증이 되지 않은 경우"},
        403: {"description": "본인이 신청하지 않은 예약을 수정하려는 경우"},
        404: {"description": "요청한 예약 ID에 대한 예약 내역이 존재하지 않는 경우"}
    }
)
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


@router.patch(
    "/{reservation_id}/confirm",
    response_model=UpdateReservationStatusResponse,
    status_code=200,
    summary="예약 확정",
    description="""
    관리자(ADMIN) 전용 기능입니다.  
    <br>예약을 확정하고, 응시 인원을 실제 시험 일정의 잔여 수용 인원에 반영합니다.
    """,
    responses={
        200: {"description": "예약 확정 성공"},
        401: {"description": "Authorization 헤더를 통한 JWT 인증이 되지 않은 경우"},
        403: {"description": "관리지가 아닌 경우"},
        404: {"description": "요청한 예약 ID에 대한 예약 내역이 존재하지 않는 경우"}
    }
)
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


@router.patch(
    "/{reservation_id}/cancel",
    response_model=UpdateReservationStatusResponse,
    status_code=200,
    summary="예약 삭제",
    description="""
    예약을 삭제(취소 처리)합니다.
    """,
    responses={
        200: {"description": "예약 삭제 성공"},
        401: {"description": "Authorization 헤더를 통한 JWT 인증이 되지 않은 경우"},
        403: {"description": "본인이 신청하지 않은 예약을 삭제하려는 경우"},
        404: {"description": "요청한 예약 ID에 대한 예약 내역이 존재하지 않는 경우"}
    }
)
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
