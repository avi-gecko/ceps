from pydantic import BaseModel, Field


class UserModel(BaseModel):
    username: str = Field(..., examples=["Alex"])
    password: str = Field(..., examples=["ALEX111"])
