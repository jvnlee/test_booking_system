from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schema.user import UserCreate, UserRead
from app.service.exception.DuplicateNameException import DuplicateNameException
from app.service.exception.DuplicateUsernameException import DuplicateUsernameException
from app.service.user import create_user


router = APIRouter()


@router.post("/", response_model=UserRead, status_code=201)
def create_user_endpoint(
        user_create: UserCreate,
        db: Session = Depends(get_db)
):
    try:
        return create_user(db, user_create)
    except (DuplicateUsernameException, DuplicateNameException) as e:
        raise HTTPException(status_code=400, detail=str(e))
