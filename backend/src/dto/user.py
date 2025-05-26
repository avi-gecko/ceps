from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    username: str = Field(..., examples=["Alex"])
    password: str = Field(..., examples=["ALEX111"])


class UserResponse(BaseModel):
    username: str
    is_active: bool


class TokenResponse(BaseModel):
    access_token: str
