from datetime import datetime, timedelta, date, time
from typing import List, Tuple
from sqlalchemy.orm import Session, joinedload
from app.model import Reservation, TestSchedule, User
from app.model.reservation import ReservationStatus
from app.model.user import UserRole
from app.exception.not_authorized_exception import NotAuthorizedException
from app.exception.not_enough_participant_capacity_exception import NotEnoughParticipantCapacityException
from app.exception.reservation_already_processed_exception import ReservationAlreadyProcessedException
from app.exception.reservation_deadline_exceeded_exception import ReservationDeadlineExceededException
from app.exception.reservation_not_found_exception import ReservationNotFoundException
from app.exception.test_schedule_not_found_exception import TestScheduleNotFoundException


def create_reservation(
        db: Session,
        user_id: int,
        desired_date: date,
        start_time: time,
        end_time: time,
        participant_num: int
) -> Reservation:
    check_reservation_deadline(desired_date)
    test_schedules = get_test_schedules(db, desired_date, start_time, end_time)

    for schedule in test_schedules:
        check_remaining_capacity(schedule, participant_num)

    new_reservation = Reservation(
        user_id=user_id,
        participant_num=participant_num
    )

    new_reservation.test_schedules = test_schedules

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation


def read_all_reservations(
        db: Session,
        limit: int,
        offset: int,
        user: User
) -> Tuple[List[Reservation], int]:
    query = db.query(Reservation).options(
        joinedload(Reservation.user),
        joinedload(Reservation.test_schedules)
    )

    if user.role != UserRole.ADMIN:
        query = query.filter(
            Reservation.user_id == user.id,
            Reservation.status != ReservationStatus.DELETED
        )

    total_count = query.count()

    reservations = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )

    return reservations, total_count


def update_reservation(
        db: Session,
        user: User,
        reservation_id: int,
        desired_date: date,
        start_time: time,
        end_time: time,
        participant_num: int,
):
    reservation = db.query(Reservation).filter(
        Reservation.id == reservation_id
    ).first()

    if not reservation:
        raise ReservationNotFoundException()

    check_authorization(reservation, user)
    check_updatable_status(reservation)
    check_reservation_deadline(desired_date)

    test_schedules = get_test_schedules(db, desired_date, start_time, end_time)
    for schedule in test_schedules:
        check_remaining_capacity(schedule, participant_num)

    reservation.test_schedules = test_schedules
    reservation.participant_num = participant_num

    db.commit()
    db.refresh(reservation)

    return reservation


def confirm_reservation(
        db: Session,
        reservation_id: int
):
    reservation = (
        db.query(Reservation)
        .options(joinedload(Reservation.test_schedules))
        .filter(Reservation.id == reservation_id)
        .first()
    )

    if not reservation:
        raise ReservationNotFoundException()

    check_updatable_status(reservation)

    participant_num = reservation.participant_num
    for schedule in reservation.test_schedules:
        check_remaining_capacity(schedule, participant_num)
        schedule.remaining_capacity -= participant_num

    reservation.status = ReservationStatus.CONFIRMED

    db.commit()


def delete_reservation(
        db: Session,
        user: User,
        reservation_id: int
):
    reservation = (
        db
        .query(Reservation)
        .filter(Reservation.id == reservation_id)
        .first()
    )

    if not reservation:
        raise ReservationNotFoundException()

    check_authorization(reservation, user)
    check_updatable_status(reservation)

    reservation.status = ReservationStatus.DELETED

    db.commit()


def check_reservation_deadline(desired_date: date):
    today = date.today()

    if desired_date - today < timedelta(days=3):
        raise ReservationDeadlineExceededException()


def get_test_schedules(db: Session, desired_date, start_time: time, end_time: time) -> List[TestSchedule]:
    start_datetime = datetime.combine(desired_date, start_time)
    end_datetime = datetime.combine(desired_date, end_time)

    test_schedules = (
        db.query(TestSchedule)
        .filter(
            TestSchedule.date_time >= start_datetime,
            TestSchedule.date_time < end_datetime
        )
        .all()
    )

    if not test_schedules:
        raise TestScheduleNotFoundException()

    return test_schedules


def check_remaining_capacity(test_schedule: TestSchedule, participant_num: int):
    if test_schedule.remaining_capacity < participant_num:
        raise NotEnoughParticipantCapacityException()


def check_authorization(reservation: Reservation, user: User):
    if user.role != UserRole.ADMIN and reservation.user_id != user.id:
        raise NotAuthorizedException()


def check_updatable_status(reservation: Reservation):
    if reservation.status != ReservationStatus.REQUESTED:
        raise ReservationAlreadyProcessedException()
