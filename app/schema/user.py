from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(..., min_length=4, max_length=20, examples=["grepp"])
    password: str = Field(..., min_length=8, max_length=20, examples=["grepp123!@"])
    name: str = Field(..., min_length=1, max_length=30, examples=["그렙"])


class UserRead(BaseModel):
    id: int
    username: str
    name: str
