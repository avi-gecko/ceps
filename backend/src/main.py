from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import FastAPI, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from src.db.session import get_session
from src.db.models import User
from src.dto.user import UserModel
from src.settings.config import settings

app = FastAPI()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_hashed_password(plain_text_password: str):
    return bcrypt.hashpw(plain_text_password.encode(), settings.SALT.encode())


def check_password(plain_text_password: str, hashed_password: bytes):
    return bcrypt.checkpw(plain_text_password.encode(), hashed_password)


@app.post("/auth")
async def login_user(data: UserModel, session: Annotated[AsyncSession, Depends(get_session)]) -> str:
    result = await session.execute(select(User).where(User.username == data.username))
    exist_user = result.scalar_one_or_none()
    if exist_user is None:
        return JSONResponse({"message": "Неверный логин или пароль"}, status_code=status.HTTP_403_FORBIDDEN)

    salt_password = get_hashed_password(data.password)
    print(salt_password)
    is_auth = check_password(data.password, salt_password)
    print(is_auth)
    if not is_auth:
        return JSONResponse({"message": "Неверный логин или пароль"}, status_code=status.HTTP_403_FORBIDDEN)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": exist_user.username}, expires_delta=access_token_expires
    )
    return JSONResponse({"token": access_token}, status_code=status.HTTP_200_OK)
