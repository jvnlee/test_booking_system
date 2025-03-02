from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schema.user import CreateUserRequest, CreateUserResponse
from app.service.user import create_user


router = APIRouter()


@router.post("/", response_model=CreateUserResponse, status_code=201)
def create_user_endpoint(
        request: CreateUserRequest,
        db: Session = Depends(get_db)
):
    new_user = create_user(
        db,
        request.username,
        request.password,
        request.name
    )

    return CreateUserResponse(
        id=new_user.id,
        username=new_user.username,
        name=new_user.name,
    )
