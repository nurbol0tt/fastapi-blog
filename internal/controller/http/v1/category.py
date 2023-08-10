from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from internal.dto.blog import CategoryRead, CategoryInput, CategoryDetailRead, CategoryReadAll
from internal.service.category import CategoryService
from internal.usecase.utils.exception import NoContentError
from internal.config.logger import logger

router = APIRouter(
    prefix='/categories',
    tags=['Category'],
)


@router.post(
    path='',
    response_model=CategoryRead,
    status_code=status.HTTP_201_CREATED
)
async def category_create(
        dto: CategoryInput,
        category_service: CategoryService = Depends()
) -> CategoryRead:
    try:
        return await category_service.create(dto)
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@router.get(
    path='',
    response_model=CategoryReadAll,
    status_code=status.HTTP_200_OK
)
async def category_list(
        application_service: CategoryService = Depends()
) -> CategoryReadAll:
    return CategoryReadAll(categories=[cs async for cs in application_service.list()])


@router.get(
    path='/{category_id}',
    response_model=CategoryDetailRead,
    status_code=status.HTTP_200_OK
)
async def category_detail(
        category_id: str,
        category_service: CategoryService = Depends()
) -> CategoryDetailRead:

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
    response_model=CategoryRead,
    status_code=status.HTTP_202_ACCEPTED
)
async def category_patch(
        dto: CategoryInput,
        category_id: str,
        category_service: CategoryService = Depends()
) -> CategoryRead:
    return await category_service.patch(category_id, dto)


@router.delete(
    path='/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def category_delete(
        category_id: str,
        category_service: CategoryService = Depends()
) -> None:
    return await category_service.delete(category_id)

