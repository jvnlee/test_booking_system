from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.service.exception.DuplicateNameException import DuplicateNameException
from app.service.exception.DuplicateUsernameException import DuplicateUsernameException
from app.service.exception.InvalidTokenException import InvalidTokenException
from app.service.exception.LoginException import LoginException
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


def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DuplicateUsernameException, bad_request_exception_handler)
    app.add_exception_handler(DuplicateNameException, bad_request_exception_handler)
    app.add_exception_handler(LoginException, bad_request_exception_handler)

    app.add_exception_handler(InvalidTokenException, unauthorized_exception_handler)

    app.add_exception_handler(TestScheduleNotFoundException, not_found_exception_handler)
