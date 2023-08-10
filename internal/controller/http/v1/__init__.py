from fastapi import APIRouter

from . import health
from . import application
from . import category
from . import auth

router = APIRouter()
router.include_router(
    health.router,
)
router.include_router(
    application.router
)
router.include_router(
    category.router,
)
router.include_router(
    auth.router,
)
