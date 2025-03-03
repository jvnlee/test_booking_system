from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token
from app.model import User
from app.service.exception.login_exception import LoginException


def login(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        raise LoginException()

    return create_access_token(username)
