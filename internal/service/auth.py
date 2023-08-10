from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker

from internal.config.database import get_session
from internal.dto.user import UserRequest, UserResponse, LoginSchema, LoginResponse, AccessTokenSchema, \
    AccessTokenResponse
from internal.repository.user import UserRepository
from internal.usecase.hashing import Hasher


class UserService:

    def __init__(
            self,
            session: async_sessionmaker = Depends(get_session),
            repository: UserRepository = Depends(),
            authorize: AuthJWT = Depends()

    ) -> None:
        self.async_session = session
        self.repository = repository
        self.authorize = authorize

    async def create(self, dto: UserRequest) -> UserResponse:
        async with self.async_session.begin() as session:
            hashed_password = Hasher.get_password_hash(dto.dict().pop("hashed_password"))
            dto_dict = dto.dict(exclude={"password"})
            dto_dict["hashed_password"] = hashed_password  # Add hashed_password to the dictionary
            user = await self.repository.create(session, **dto_dict)
            return UserResponse.from_orm(user)

    async def login(self, dto: LoginSchema) -> LoginResponse:
        async with self.async_session.begin() as session:
            token = await self.repository.login(self.authorize, session, **dto.dict())
            return LoginResponse.from_orm(token)

    async def refresh_token(self, dto: AccessTokenSchema) -> AccessTokenResponse:
        async with self.async_session.begin() as session:
            refresh_token = await self.repository.refresh_token(self.authorize, session, **dto.dict())
            return AccessTokenResponse.from_orm(refresh_token)
