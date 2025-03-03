from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=4,
        max_length=20,
        examples=["grepp"],
        description="로그인에 사용할 아이디"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        examples=["grepp123!@"],
        description="로그인에 사용할 비밀번호"
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=30,
        examples=["그렙"],
        description="이름 (기업 고객의 경우 회사명 사용)"
    )


class CreateUserResponse(BaseModel):
    username: str = Field(
        ...,
        examples=["grepp"],
        description="로그인에 사용할 아이디"
    )
    name: str = Field(
        ...,
        examples=["그렙"],
        description="이름 (기업 고객의 경우 회사명 사용)"
    )
