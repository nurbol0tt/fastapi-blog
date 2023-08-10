from typing import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from internal.config.database import get_session
from internal.dto.blog import BaseApplication, ApplicationRead, ApplicationInput, CategoryRead, ApplicationDetailRead
from internal.repository.application import ApplicationRepository


# class ApplicationService:
#
#     def __init__(self, repository: ApplicationRepository = Depends()) -> None:
#         self.repository = repository
#
#     async def create(self, dto: BaseApplication) -> ApplicationRead:
#         application = await self.repository.create(**dto.dict())
#         return ApplicationRead.from_orm(application)
#
#     async def list(self) -> AsyncIterator[ApplicationRead]:
#         async for application in self.repository.list():
#             yield ApplicationRead.from_orm(application)
#
#     async def retrieve(self, application_id: str) -> ApplicationRead:
#         application = await self.repository.retrieve(application_id)
#         return ApplicationRead.from_orm(application)
#
#     async def put(self, application_id: str, dto: BaseApplication) -> ApplicationRead:
#         application = await self.repository.update(application_id, **dto.dict())
#         return ApplicationRead.from_orm(application)
#
#     async def delete(self, application_id: str) -> None:
#         await self.repository.delete(application_id)


class ApplicationService:

    def __init__(
            self,
            session: async_sessionmaker = Depends(get_session),
            repository: ApplicationRepository = Depends(),
    ) -> None:
        self.async_session = session
        self.repository = repository

    async def create(self, dto: ApplicationInput) -> ApplicationRead:
        async with self.async_session.begin() as session:
            application = await self.repository.create(session, **dto.dict())
            return ApplicationRead.from_orm(application)

    async def list(self) -> AsyncIterator[ApplicationRead]:
        async with self.async_session.begin() as session:
            async for application in self.repository.list(session):

                yield ApplicationRead.from_orm(application)

    async def retrieve(self, application_id: str) -> ApplicationDetailRead:
        async with self.async_session.begin() as session:
            application = await self.repository.retrieve(session, application_id)
            return ApplicationDetailRead.from_orm(application)

    async def put(self, application_id: str, dto: ApplicationInput) -> ApplicationRead:
        async with self.async_session.begin() as session:
            application = await self.repository.put(session, application_id, **dto.dict())
            return ApplicationRead.from_orm(application)

    async def delete(self, application_id: str) -> None:
        async with self.async_session.begin() as session:
            await self.repository.delete(session, application_id)
