import os
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.model import TestSchedule
from app.model.user import User, UserRole
from app.core.security import hash_password


# users 테이블에 admin user 레코드 1개 삽입
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
            role=UserRole.ADMIN
        )
        db.add(new_admin)
        db.commit()

    db.close()


# test_schedules 테이블에 더미 데이터 삽입
def init_test_schedules():
    db: Session = SessionLocal()

    try:
        start_date = datetime(2025, 3, 1, 0)
        end_date = datetime(2025, 3, 31, 23)

        schedules = []
        current_time = start_date

        while current_time <= end_date:
            schedules.append(TestSchedule(time=current_time))
            current_time += timedelta(hours=1)

        db.bulk_save_objects(schedules)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()
