from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model: type[Any] = None

    @classmethod
    async def find_all(cls, session: AsyncSession):
        result = await session.execute(select(cls.model))
        return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, item_id: int):
        result = await session.execute(select(cls.model).where(cls.model.id == item_id))
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filters):
        result = await session.execute(select(cls.model).filter_by(**filters))
        return result.scalar_one_or_none()

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        obj = cls.model(**values)
        session.add(obj)
        await session.commit()
        return obj
