from pydantic import Field

from src.dto.base import BaseDTO


class UserRequest(BaseDTO):
    username: str = Field(..., examples=["Alex"])
    password: str = Field(..., examples=["ALEX111"])


class UserResponse(BaseDTO):
    username: str
    is_active: bool


class TokenResponse(BaseDTO):
    access_token: str
