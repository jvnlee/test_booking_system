from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=4, max_length=20, examples=["grepp"])
    password: str = Field(..., min_length=8, max_length=20, examples=["grepp123!@"])


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
