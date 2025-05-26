from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_session
from src.db.models import User
from src.dto.user import UserRequest, TokenResponse, UserResponse
from src.settings.config import settings

app = FastAPI()

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


@app.post("/auth")
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


@app.get("/protected/test")
async def test(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user
