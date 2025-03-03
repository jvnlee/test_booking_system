from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schema.login import LoginResponse, LoginRequest
from app.service.login import login

router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=200,
    summary="로그인",
    description="""  
    로그인 성공 응답으로 받은 JWT Access Token을 Authorization 헤더에 넣어 요청을 보내면 인증이 필요한 API 호출이 가능해집니다.  
    <br>토큰은 Authorization: Bearer \<token\> 형태로 사용합니다.
    """
)
def login_endpoint(
        request: LoginRequest,
        db: Session = Depends(deps.get_db)
):
    access_token = login(db, request.username, request.password)

    return LoginResponse(
        access_token=access_token,
        token_type="Bearer"
    )
