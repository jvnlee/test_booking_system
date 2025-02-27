import os

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.model.user import User, RoleEnum
from app.core.security import hash_password


def init_admin():
    db: Session = SessionLocal()
    admin_user = (db
                  .query(User)
                  .filter(User.username == os.getenv("ADMIN_USERNAME"))
                  .first())

    if not admin_user:
        new_admin = User(
            username="admin",
            password=hash_password(os.getenv("ADMIN_PASSWORD")),
            name="관리자",
            role=RoleEnum.admin
        )
        db.add(new_admin)
        db.commit()

    db.close()
