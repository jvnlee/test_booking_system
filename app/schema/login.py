from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(
        ...,
        min_length=4,
        max_length=20,
        examples=["grepp"],
        description="로그인 아이디"
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=20,
        examples=["grepp123!@"],
        description="로그인 비밀번호"
    )


class LoginResponse(BaseModel):
    access_token: str = Field(
        ...,
        alias="accessToken",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbmR5MTIzNCIsImlhdCI6MTc0MTAzNzA1OCwiZXhwIjoxNzQxMDM4ODU4fQ.EsTSjWMPrdmx8GSLtNd_C4r5QLdcTk4tDmdhg9BKvNY"],
        description="JWT 액세스 토큰"
    )
    token_type: str = Field(
        ...,
        alias="tokenType",
        examples=["Bearer"],
        description="토큰 타입"
    )

    class Config:
        populate_by_name = True
        by_alias = True
