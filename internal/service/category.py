from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from internal.config.database import get_session
from internal.dto.blog import CategoryInput, CategoryRead, CategoryDetailRead
from internal.repository.category import CategoryRepository


class CategoryService:

    def __init__(
            self,
            session: async_sessionmaker = Depends(get_session),
            repository: CategoryRepository = Depends()
    ) -> None:
        self.async_session = session
        self.repository = repository

    async def create(self, dto: CategoryInput) -> CategoryRead:
        async with self.async_session.begin() as session:
            category = await self.repository.create(session, **dto.dict())
            return CategoryRead.from_orm(category)

    async def list(self) -> AsyncIterator[CategoryRead]:
        async with self.async_session.begin() as session:
            async for category in self.repository.list(session):
                yield CategoryRead.from_orm(category)

    async def retrieve(self, category_id: str) -> CategoryDetailRead:
        async with self.async_session.begin() as session:
            category = await self.repository.retrieve(session, category_id)
            return CategoryDetailRead.from_orm(category)

    async def patch(self, category_id: str, dto: CategoryInput) -> CategoryRead:
        async with self.async_session.begin() as session:
            category = await self.repository.patch(session, category_id, **dto.dict())
            return CategoryRead.from_orm(category)

    async def delete(self, category_id: str) -> None:
        async with self.async_session.begin() as session:
            await self.repository.delete(session, category_id)
