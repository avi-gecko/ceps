from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.settings.config import settings


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine = create_async_engine(settings.POSTGRES_URL)
    async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
