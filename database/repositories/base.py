"""Generic repository helpers."""
from __future__ import annotations
from typing import Generic, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.base import Base

ModelT = TypeVar("ModelT", bound=Base)
class Repository(Generic[ModelT]):
    model: type[ModelT]
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    async def get(self, pk: object) -> ModelT | None:
        return await self.session.get(self.model, pk)
    async def add(self, obj: ModelT) -> ModelT:
        self.session.add(obj); await self.session.flush(); return obj
    async def list(self, limit: int = 50, offset: int = 0) -> list[ModelT]:
        result = await self.session.scalars(select(self.model).limit(limit).offset(offset))
        return list(result)
