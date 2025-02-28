from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.service.exception.DuplicateUsernameException import DuplicateUsernameException
from app.service.exception.DuplicateNameException import DuplicateNameException
from app.service.exception.LoginException import LoginException


def bad_request_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DuplicateUsernameException, bad_request_exception_handler)
    app.add_exception_handler(DuplicateNameException, bad_request_exception_handler)
    app.add_exception_handler(LoginException, bad_request_exception_handler)
