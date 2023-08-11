from asyncpg import UniqueViolationError
from fastapi import APIRouter, Depends, HTTPException, Path, Response
from sqlalchemy.exc import IntegrityError
from starlette import status

from internal.config.logger import logger
from internal.service.blog_service import ApplicationService
from internal.usecase.utils.exception import NoContentError, DuplicateError
from internal.dto.blog import (
    ApplicationDetailRead,
    ApplicationResponse,
    ApplicationReadAllResponse,
    ApplicationRequest,
)

router = APIRouter(
    prefix='/blogs',
    tags=['Application'],
)


@router.post(
    path='',
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
async def application_create(
        dto: ApplicationRequest,
        application_service: ApplicationService = Depends()
) -> ApplicationResponse:
    try:
        return await application_service.create(dto)
    except (UniqueViolationError, IntegrityError) as error:
        logger.info(f"Email or phone already exists.: {error}")
        raise HTTPException(409, detail="Email or phone already exists.")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@router.get(
    path='',
    response_model=ApplicationReadAllResponse,
    status_code=status.HTTP_200_OK,
)
async def application_list(
        application_service: ApplicationService = Depends()
) -> ApplicationReadAllResponse:

    try:
        application = ApplicationReadAllResponse(
            applications=[ap async for ap in application_service.list()]
        )
    except NoContentError as e:
        logger.info(f"NoContentError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return application


@router.get(
    path='/{application_id}',
    response_model=ApplicationDetailRead,
    status_code=status.HTTP_200_OK,
)
async def application_retrieve(
        application_id: str,
        application_service: ApplicationService = Depends()
) -> ApplicationDetailRead:

    try:
        application = await application_service.retrieve(application_id)
    except NoContentError as e:
        logger.info(f"NonContentError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return application


@router.put(
    path='/{application_id}',
    response_model=ApplicationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        204: {
            "description": "User is updated, but data fetch is failed.",
        }
    }
)
async def application_put(
        dto: ApplicationRequest,
        application_id: str = Path(title="The ID of the application"),
        application_service: ApplicationService = Depends()
) -> ApplicationResponse:

    try:
        content = await application_service.put(application_id, dto)
    except DuplicateError as e:
        logger.info(f"DuplicateError: {e}")
        raise HTTPException(status_code=409, detail=f"User or email is already exists: {dto}")
    except NoContentError as e:
        if "404" in str(e):
            logger.info(f"NoContentError: User not found: id={id}")
            raise HTTPException(status_code=404, detail=f"User not found: id={id}")
        else:
            logger.warning(f"NoContentError: User({dto}) is updated, but data fetch is failed.")
            return Response(status_code=204)
    except ValueError as e:
        logger.info(f"ValueError: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content


@router.delete(
    path='/{application_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def application_delete(
        application_id: str,
        application_service: ApplicationService = Depends()
) -> None:

    try:
        content = await application_service.delete(application_id)
    except NoContentError:
        logger.info(f"NoContentError: User not found: id={id}")
        raise HTTPException(status_code=404, detail=f"User not found: id={id}")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return content
