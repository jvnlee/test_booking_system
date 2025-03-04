from fastapi import Depends, Request
from sqlalchemy.orm import Session
from app.core.security import get_payload_from_access_token
from app.db.session import SessionLocal
from app.model import User
from app.model.user import UserRole
from app.exception.invalid_token_exception import InvalidTokenException
from app.exception.not_authorized_exception import NotAuthorizedException


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_token_from_request(request: Request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise InvalidTokenException()

    return auth_header.split("Bearer ")[1]


def get_current_user(
        token: str = Depends(get_token_from_request),
        db: Session = Depends(get_db)
):
    payload = get_payload_from_access_token(token)

    if payload is None:
        raise InvalidTokenException()

    username = payload.get("sub")

    if not username:
        raise InvalidTokenException()

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise InvalidTokenException()

    return user


def is_admin_user(user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise NotAuthorizedException()

    return user
