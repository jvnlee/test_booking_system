from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schema.user import UserCreate, UserRead
from app.service.user import create_user

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=201)
def create_user_endpoint(
        user_create: UserCreate,
        db: Session = Depends(get_db)
):
    return create_user(db, user_create)
