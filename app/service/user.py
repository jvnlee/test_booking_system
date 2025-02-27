from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.security import hash_password
from app.model.user import User
from app.schema.user import UserCreate
from app.service.exception.DuplicateNameException import DuplicateNameException
from app.service.exception.DuplicateUsernameException import DuplicateUsernameException


def create_user(db: Session, user_create: UserCreate) -> User:
    check_duplicate_user_info(db, user_create)

    hashed_password = hash_password(user_create.password)

    new_user = User(
        username=user_create.username,
        password=hashed_password,
        name=user_create.name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def check_duplicate_user_info(db: Session, user_create: UserCreate) -> None:
    existing_user = (db
                     .query(User)
                     .filter(or_(User.username == user_create.username,
                                 User.name == user_create.name))
                     .first())

    if existing_user:
        if existing_user.username == user_create.username:
            raise DuplicateUsernameException()
        if existing_user.name == user_create.name:
            raise DuplicateNameException()
