from datetime import timedelta

from starlette import status

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from internal.config import settings
from internal.entity.user_entity import User
from internal.usecase.hashing import Hasher


class UserRepository:

    async def create(self, session: AsyncSession, **kwargs):
        user = User(**kwargs)
        session.add(user)
        await session.flush()
        return user

    async def login(self, authorize, session: AsyncSession, **kwargs):
        user = select(User).where(User.email == kwargs['email'])
        user = await session.scalar(user)

        if not Hasher.verify_password(kwargs['hashed_password'], user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Email or Password",
            )
        user.access_token = await authorize.create_access_token(
            subject=str(user.username), expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
        )
        user.refresh_token = await authorize.create_refresh_token(
            subject=str(user.username), expires_time=timedelta(days=settings.REFRESH_TOKEN_EXPIRES_IN)
        )
        return user

    async def refresh_token(self, authorize, session: AsyncSession):
        try:
            await authorize.jwt_refresh_token_required()
            username = await authorize.get_jwt_subject()
            user = await session.scalar(select(User).where(User.username == username))
            user.access_token = await authorize.create_access_token(subject=str(user.id))
            return user
        except Exception as e:
            error = e.__class__.__name__
            if error == "MissingTokenError":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Please provide refresh token",
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error
            )

    async def get_me(self, authorize, session: AsyncSession):
        await authorize.jwt_required()
        username = await authorize.get_jwt_subject()
        return await session.scalar(select(User).where(User.username == username))
