"""Async database engine and session factory."""
from __future__ import annotations
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import get_settings

settings = get_settings()
engine_kwargs = {"echo": settings.debug, "pool_pre_ping": True}
if not settings.database_url.startswith("sqlite"):
    engine_kwargs.update(pool_size=settings.database_pool_size, max_overflow=settings.database_max_overflow, pool_recycle=settings.database_pool_recycle_seconds)
engine = create_async_engine(settings.database_url, **engine_kwargs)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
