from abc import ABC, abstractmethod
from typing import AsyncIterator

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from internal.entity.blog import Blog
# from internal.entity.blog import Application
from internal.usecase.hashing import Hasher


class ApplicationABC(ABC):

    @abstractmethod
    async def create(self, **kwargs) -> Blog:
        ...

    @abstractmethod
    async def retrieve(self, application_id: str) -> Blog:
        ...

    @abstractmethod
    async def update(self, application_id: str) -> Blog:
        ...

    @abstractmethod
    async def delete(self, application_id: str) -> None:
        ...


# class ApplicationRepository(ApplicationABC):
#
#     def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
#         self.session = session
#
#     async def create(self, **kwargs) -> Application:
#         application = Application(**kwargs)
#         self.session.add(application)
#         await self.session.flush()
#         return application
#
#     async def list(self) -> AsyncIterator[Application]:
#         stmt = select(Application)
#         stream = await self.session.stream_scalars(stmt.order_by(Application.id))
#         async for row in stream:
#             yield row
#
#     async def retrieve(self, application_id: str) -> Application:
#         stmt = select(Application).where(Application.id == application_id)
#         return await self.session.scalar(stmt.order_by(Application.id))
#
#     async def update(self, application_id: str, **kwargs) -> Application:
#         stmt = update(Application).where(Application.id == application_id).values(**kwargs)
#         await self.session.execute(stmt)
#         await self.session.flush()
#         return await self.retrieve(application_id)
#
#     async def delete(self, application_id: str) -> None:
#         statement = select(Application).where(Application.id == application_id)
#         result = await self.session.execute(statement)
#         application_id = result.scalar_one_or_none()
#         await self.session.delete(application_id)
#         await self.session.flush()


class ApplicationRepository:

    @classmethod
    async def create(cls, session: AsyncSession,  **kwargs):
        application = Blog(**kwargs)
        session.add(application)
        await session.flush()
        return application

    @classmethod
    async def list(cls, session: AsyncSession) -> AsyncIterator[Blog]:
        stmt = select(Blog)
        stream = await session.stream_scalars(stmt.order_by(Blog.id))
        async for row in stream:
            yield row

    @classmethod
    async def retrieve(cls, session: AsyncSession, application_id: str):
        stmt = select(Blog).where(Blog.id == application_id)
        return await session.scalar(stmt)

    @classmethod
    async def put(cls, session: AsyncSession, application_id: str, **kwargs) -> Blog:
        stmt = update(Blog).where(Blog.id == application_id).values(**kwargs)
        await session.execute(stmt)
        await session.flush()
        return await cls.retrieve(session, application_id)

    @classmethod
    async def delete(cls, session: AsyncSession, application_id: str) -> None:
        statement = select(Blog).where(Blog.id == application_id)
        result = await session.execute(statement)
        application_id = result.scalar_one_or_none()
        await session.delete(application_id)
        await session.flush()

