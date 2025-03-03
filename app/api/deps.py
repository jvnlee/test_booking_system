from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import get_payload_from_access_token
from app.db.session import SessionLocal
from app.model import User
from app.model.user import UserRole
from app.service.exception.invalid_token_exception import InvalidTokenException
from app.service.exception.not_authorized_exception import NotAuthorizedException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_current_user(
        token: str = Depends(oauth2_scheme),
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
