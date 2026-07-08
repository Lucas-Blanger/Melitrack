import uuid

from fastapi import APIRouter, Depends, File, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.hives.schemas import (
    AnalysisResponse,
    InspectionCreate,
    InspectionResponse,
    PhotoResponse,
)
from apps.hives.services import inspection_service, photo_service
from core.dependencies import get_current_user, get_db, get_mongo_db

router = APIRouter(prefix="/inspections", tags=["inspections"])


@router.post("", response_model=InspectionResponse, status_code=status.HTTP_201_CREATED)
async def create_inspection(
    payload: InspectionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await inspection_service.create_inspection(db, current_user.id, payload)


@router.get("/hive/{hive_id}", response_model=list[InspectionResponse])
async def list_inspections_by_hive(
    hive_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await inspection_service.list_inspections_by_hive(
        db,
        current_user.id,
        hive_id,
    )


@router.get("/{inspection_id}", response_model=InspectionResponse)
async def get_inspection(
    inspection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await inspection_service.get_inspection(
        db,
        current_user.id,
        inspection_id,
    )


@router.post(
    "/{inspection_id}/photos",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_inspection_photo(
    inspection_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db),
    current_user: User = Depends(get_current_user),
):
    inspection = await inspection_service.get_inspection(
        db,
        current_user.id,
        inspection_id,
    )

    photo = await photo_service.upload_inspection_photo(
        mongo,
        current_user.id,
        inspection.hive_id,
        inspection.id,
        file,
    )

    await inspection_service.ensure_pending_analysis(db, inspection.id)

    return photo


@router.get("/{inspection_id}/analysis", response_model=AnalysisResponse)
async def get_inspection_analysis(
    inspection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await inspection_service.get_inspection_analysis(
        db,
        current_user.id,
        inspection_id,
    )
