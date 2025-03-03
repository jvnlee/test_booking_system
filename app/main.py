from fastapi import FastAPI
from app.api.endpoints import user, login, test_schedule, reservation
from app.core.exception_handler import register_exception_handlers
from app.db.init import initialize_database


initialize_database()

app = FastAPI(
    title="Test Booking System",
    description="시험 일정 예약 시스템"
)

register_exception_handlers(app)

app.include_router(
    user.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    login.router,
    tags=["Login"]
)

app.include_router(
    test_schedule.router,
    prefix="/test-schedules",
    tags=["Test Schedules"]
)

app.include_router(
    reservation.router,
    prefix="/reservations",
    tags=["Reservations"]
)