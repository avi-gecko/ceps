from typing import Annotated

from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.models import User
from src.settings.config import settings
from src.dto.user import UserResponse
from src.db.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_hashed_password(plain_text_password: str):
    return bcrypt.hashpw(plain_text_password.encode(), settings.SALT.encode())


def check_password(plain_text_password: str, hashed_password: bytes):
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    result = await session.execute(select(User).where(User.username == username))
    exist_user = result.scalar_one_or_none()
    if exist_user is None:
        raise credentials_exception
    return UserResponse(username=exist_user.username, is_active=exist_user.is_active)


async def get_current_active_user(
    current_user: Annotated[UserResponse, Depends(get_current_user)],
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Пользователь не активный")
    return current_user
