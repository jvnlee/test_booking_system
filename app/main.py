from fastapi import FastAPI
from app.api.endpoints import user
from app.db.init_admin import init_admin


init_admin()

app = FastAPI(
    title="Test Booking System",
    description="시험 일정 예약 시스템"
)

app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"]
)