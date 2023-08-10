from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette import status

from internal.config.logger import logger
from internal.service.auth import UserService
from internal.dto.user import (
    UserResponse,
    UserRequest,
    LoginSchema,
    LoginResponse,
    AccessTokenResponse,
    AccessTokenSchema
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


# @router.get(
#     path='/me',
#     response_model=UserResponse
# )
# async def get_me(
#     user: User = Depends(require_user),
# ):
#     return user


@router.post(
    path='logout'
)
async def logout(

):
    ...


@router.post(
    path='/refresh',
    response_model=AccessTokenResponse
)
async def refresh_token(
    dto: AccessTokenSchema,
    user_service: UserService = Depends()
) -> AccessTokenResponse:
    try:
        return await user_service.refresh_token(dto)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

