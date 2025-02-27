from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.service.exception.DuplicateUsernameException import DuplicateUsernameException
from app.service.exception.DuplicateNameException import DuplicateNameException


def duplicate_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(DuplicateUsernameException, duplicate_exception_handler)
    app.add_exception_handler(DuplicateNameException, duplicate_exception_handler)
