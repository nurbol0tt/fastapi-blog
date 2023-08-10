import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncGenerator, Callable, AsyncIterator

from sqlalchemy import create_engine, orm
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from internal.config import settings
from internal.entity.base import Base
from internal.usecase.utils.mocks import get_session

AsyncSessionGenerator = AsyncGenerator[AsyncSession, None]

logger = logging.getLogger(__name__)


async def create_database(url: str) -> None:
    engine = create_async_engine(
        url, pool_pre_ping=True, future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


def async_session(
    url: str, *, wrap: Callable[..., Any] | None = None,
) -> Callable[..., AsyncSessionGenerator] | AsyncContextManager[Any]:
    engine = create_async_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False,
    )

    async def get_session() -> AsyncSessionGenerator:  # noqa: WPS430, WPS442
        async with factory() as session:
            yield session

    return get_session if wrap is None else wrap(get_session)


def sync_session(url: str) -> orm.scoped_session:
    engine = create_engine(
        url, pool_pre_ping=True, future=True,
    )
    factory = orm.sessionmaker(
        engine, autoflush=False, expire_on_commit=False,
    )
    return orm.scoped_session(factory)


override_session = get_session, async_session(settings.DATABASE_URI)
current_session = sync_session(settings.DATABASE_URI.replace('+asyncpg', ''))
context_session = async_session(settings.DATABASE_URI, wrap=asynccontextmanager)

async_engine = create_async_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)


# async_session = sessionmaker(
#     bind=async_engine,
#     class_=AsyncSession,
#     expire_on_commit=False
# )
