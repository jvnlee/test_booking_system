from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.model.user import User
from app.service.exception.DuplicateNameException import DuplicateNameException
from app.service.exception.DuplicateUsernameException import DuplicateUsernameException


def create_user(db: Session, username: str, password: str, name: str) -> User:
    check_duplicate_user_info(db, username, name)

    hashed_password = hash_password(password)

    new_user = User(
        username=username,
        password=hashed_password,
        name=name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def check_duplicate_user_info(db: Session, username: str, name: str) -> None:
    existing_user = (db
                     .query(User)
                     .filter(or_(User.username == username,
                                 User.name == name))
                     .first())

    if existing_user:
        if existing_user.username == username:
            raise DuplicateUsernameException()
        if existing_user.name == name:
            raise DuplicateNameException()
