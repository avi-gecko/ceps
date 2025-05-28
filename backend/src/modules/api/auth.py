from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.settings.config import settings
from src.db.models import User
from src.db.session import get_session
from src.dto.user import UserRequest, TokenResponse, UserResponse
from src.modules.auth.utils import (
    check_password,
    create_access_token,
    get_hashed_password,
    get_current_user,
)

router = APIRouter(tags=["auth"])


@router.post("/auth")
async def login_user(
    data: UserRequest, session: Annotated[AsyncSession, Depends(get_session)]
) -> TokenResponse:
    forbidden_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Неверный логин или пароль"
    )
    result = await session.execute(select(User).where(User.username == data.username))
    exist_user = result.scalar_one_or_none()
    if exist_user is None:
        return forbidden_exception

    salt_password = get_hashed_password(data.password)
    is_auth = check_password(data.password, salt_password)
    if not is_auth:
        return forbidden_exception

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": exist_user.username}, expires_delta=access_token_expires
    )
    await session.execute(
        update(User).where(User.username == data.username).values(is_active=True)
    )
    return TokenResponse(access_token=access_token)


@router.post("/is_auth")
async def is_auth(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    return current_user
