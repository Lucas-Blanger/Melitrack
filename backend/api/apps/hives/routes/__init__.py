from fastapi import APIRouter

from .dashboard import router as dashboard_router
from .harvests import router as harvests_router
from .hives import router as hives_router
from .inspections import router as inspections_router
from .product import router as product_router

router = APIRouter()

router.include_router(hives_router)
router.include_router(inspections_router)
router.include_router(harvests_router)
router.include_router(dashboard_router)
router.include_router(product_router)
