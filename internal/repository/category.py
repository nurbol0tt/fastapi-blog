from abc import ABC, abstractmethod
from typing import AsyncIterator

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from internal.entity.blog_entity import Blog, Category


class CategoryABC(ABC):

    @abstractmethod
    async def create(self, **kwargs) -> Category:
        ...


class CategoryRepository:

    async def create(self, session: AsyncSession, **kwargs):
        category = Category(**kwargs)
        session.add(category)
        await session.flush()
        return category

    async def list(self, session: AsyncSession) -> AsyncIterator[Blog]:
        stmt = select(Category)
        stream = await session.stream_scalars(stmt.order_by(Category.id))
        async for row in stream:
            yield row

    async def retrieve(self, session: AsyncSession, category_id: str):
        stmt = select(Category).where(Category.id == category_id)
        return await session.scalar(stmt.order_by(Category.id))

    async def patch(self, session: AsyncSession, category_id: str, **kwargs):
        query = (
            update(Category)
            .where(Category.id == category_id)
            .values(**kwargs)
            .returning(Category)
        )
        await session.execute(query)
        await session.flush()
        return await self.retrieve(session, category_id)

    async def delete(self, session: AsyncSession, category_id: str) -> None:
        statement = select(Category).where(Category.id == category_id)
        result = await session.execute(statement)
        application_id = result.scalar_one_or_none()
        await session.delete(application_id)
        await session.flush()
