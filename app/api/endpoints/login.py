from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schema.login import LoginResponse, LoginRequest
from app.service.login import login

router = APIRouter()


@router.post("/login", response_model=LoginResponse, status_code=200)
def login_endpoint(
        request: LoginRequest,
        db: Session = Depends(deps.get_db)
):
    access_token = login(db, request.username, request.password)

    return LoginResponse(access_token=access_token)
