from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.hives.schemas import DashboardOverview
from apps.hives.services import dashboard_service
from core.dependencies import get_current_user, get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await dashboard_service.get_dashboard_overview(db, current_user.id)
