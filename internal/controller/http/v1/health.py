from fastapi import APIRouter

from internal.usecase.utils.responses import SuccessfulResponse

router = APIRouter(
    prefix='/health',
    tags=['Health'],
)


@router.get('', responses=SuccessfulResponse.schema())
async def health() -> SuccessfulResponse:
    return SuccessfulResponse()
