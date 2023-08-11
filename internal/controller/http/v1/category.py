from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from internal.dto.blog import CategoryResponse, CategoryRequest, CategoryDetailResponse, CategoryAllResponse
from internal.service.category import CategoryService
from internal.usecase.utils.exception import NoContentError
from internal.config.logger import logger

router = APIRouter(
    prefix='/categories',
    tags=['Category'],
)


@router.post(
    path='',
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED
)
async def category_create(
        dto: CategoryRequest,
        category_service: CategoryService = Depends()
) -> CategoryResponse:
    try:
        return await category_service.create(dto)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@router.get(
    path='',
    response_model=CategoryAllResponse,
    status_code=status.HTTP_200_OK
)
async def category_list(
        application_service: CategoryService = Depends()
) -> CategoryAllResponse:
    return CategoryAllResponse(
        categories=[cs async for cs in application_service.list()]
    )


@router.get(
    path='/{category_id}',
    response_model=CategoryDetailResponse,
    status_code=status.HTTP_200_OK
)
async def category_detail(
        category_id: str,
        category_service: CategoryService = Depends()
) -> CategoryDetailResponse:

    try:
        category = await category_service.retrieve(category_id)
    except NoContentError as e:
        logger.info(f"NonContentError: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return category


@router.patch(
    path='/{category_id}',
    response_model=CategoryResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def category_patch(
        dto: CategoryRequest,
        category_id: str,
        category_service: CategoryService = Depends()
) -> CategoryResponse:
    return await category_service.patch(category_id, dto)


@router.delete(
    path='/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def category_delete(
        category_id: str,
        category_service: CategoryService = Depends()
) -> None:

    try:
        content = await category_service.delete(category_id)
    except NoContentError:
        logger.info(f"NoContentError: Category not found: id={id}")
        raise HTTPException(status_code=404, detail=f"User not found: id={id}")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return content
