from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status
from starlette.responses import Response

from internal.config.logger import logger
from internal.service.auth import UserService
from internal.dto.user import (
    UserResponse,
    UserRequest,
    LoginSchema,
    LoginResponse,
    AccessTokenResponse,
)

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post(
    path='/register',
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def user_create(
        dto: UserRequest,
        user_service: UserService = Depends()
):
    try:
        return await user_service.create(dto)
    except (UniqueViolationError, IntegrityError) as error:
        logger.info(f"Email or phone already exists.: {error}")
        raise HTTPException(409, detail="Email or phone already exists.")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@router.post(
    path='/login',
    response_model=LoginResponse
)
async def login(
        dto: LoginSchema,
        user_service: UserService = Depends()
) -> LoginResponse:
    try:
        return await user_service.login(dto)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@router.get(
    path='/me',
    response_model=UserResponse
)
async def get_me(
        user_service: UserService = Depends(),
        status_code=status.HTTP_200_OK
) -> UserResponse:
    try:
        return await user_service.get_me()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post(
    path='/logout',
    status_code=status.HTTP_200_OK
)
async def logout(
        authorize: AuthJWT = Depends(),
):
    ...
    # try:
    #     await authorize.jwt_required()  # Ensure the user is authenticated
    #     await authorize.expire_jwt_token()  # Clear JWT cookies to log the user out
    #     return {"message": "Logged out successfully"}
    # except AuthJWTException as e:
    #     raise HTTPException(status_code=e.status_code, detail=str(e))


@router.post(
    path='/refresh',
    response_model=AccessTokenResponse
)
async def refresh_token(
    user_service: UserService = Depends()
) -> AccessTokenResponse:
    try:
        return await user_service.refresh_token()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

