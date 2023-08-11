from fastapi import APIRouter

from . import health
from . import blog
from . import category
from . import auth

router = APIRouter()
router.include_router(
    health.router,
)
router.include_router(
    blog.router
)
router.include_router(
    category.router,
)
router.include_router(
    auth.router,
)
