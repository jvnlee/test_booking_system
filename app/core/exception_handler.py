from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.service.exception.duplicate_name_exception import DuplicateNameException
from app.service.exception.duplicate_username_exception import DuplicateUsernameException
from app.service.exception.invalid_token_exception import InvalidTokenException
from app.service.exception.login_exception import LoginException
from app.service.exception.not_authorized_exception import NotAuthorizedException
from app.service.exception.not_enough_participant_capacity_exception import NotEnoughParticipantCapacityException
from app.service.exception.reservation_already_processed_exception import ReservationAlreadyProcessedException
from app.service.exception.reservation_deadline_exceeded_exception import ReservationDeadlineExceededException
from app.service.exception.reservation_not_found_exception import ReservationNotFoundException
from app.service.exception.test_schedule_not_found_exception import TestScheduleNotFoundException


def bad_request_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


def unauthorized_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
        content={"detail": str(exc)}
    )


def forbidden_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)}
    )


def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


def register_exception_handlers(app: FastAPI):
    # 400
    app.add_exception_handler(DuplicateUsernameException, bad_request_exception_handler)
    app.add_exception_handler(DuplicateNameException, bad_request_exception_handler)
    app.add_exception_handler(LoginException, bad_request_exception_handler)
    app.add_exception_handler(NotEnoughParticipantCapacityException, bad_request_exception_handler)
    app.add_exception_handler(ReservationAlreadyProcessedException, bad_request_exception_handler)
    app.add_exception_handler(ReservationDeadlineExceededException, bad_request_exception_handler)

    # 401
    app.add_exception_handler(InvalidTokenException, unauthorized_exception_handler)

    # 403
    app.add_exception_handler(NotAuthorizedException, forbidden_exception_handler)

    # 404
    app.add_exception_handler(TestScheduleNotFoundException, not_found_exception_handler)
    app.add_exception_handler(ReservationNotFoundException, not_found_exception_handler)
