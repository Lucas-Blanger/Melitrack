import uuid
from datetime import date

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.hives.schemas import HarvestCreate, HarvestResponse, HarvestSummaryResponse
from apps.hives.services import harvest_service
from core.dependencies import get_current_user, get_db

router = APIRouter(prefix="/harvests", tags=["harvests"])


@router.post("", response_model=HarvestResponse, status_code=status.HTTP_201_CREATED)
async def create_harvest(
    payload: HarvestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await harvest_service.create_harvest(db, current_user.id, payload)


@router.get("/hive/{hive_id}", response_model=list[HarvestResponse])
async def list_harvests_by_hive(
    hive_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await harvest_service.list_harvests_by_hive(
        db,
        current_user.id,
        hive_id,
    )


@router.get("/summary", response_model=HarvestSummaryResponse)
async def get_harvest_summary(
    start_date: date | None = Query(None),
    end_date: date | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await harvest_service.get_harvest_summary(
        db,
        current_user.id,
        start_date,
        end_date,
    )
