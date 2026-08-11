import secrets
import uuid

import httpx
from fastapi import APIRouter, Depends, File, Header, Request, UploadFile, status

from core.logger import get_logger
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.hives.schemas import (
    AnalysisResponse,
    AnalysisUpdate,
    InspectionCreate,
    InspectionResponse,
    PhotoResponse,
)
from apps.hives.services import inspection_service, photo_service
from config import get_settings
from core.dependencies import (
    get_current_user,
    get_db,
    get_mongo_db,
    get_current_user_or_ml_service,
)

settings = get_settings()
logger = get_logger(__name__)

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

    await file.seek(0)
    image_bytes = await file.read()

    if settings.ML_SERVICE_URL and settings.ML_SERVICE_TOKEN:
        ml_service_urls = [settings.ML_SERVICE_URL]
        if settings.ML_SERVICE_URL.endswith(":8000"):
            ml_service_urls.append("http://host.docker.internal:8003")

        last_error: Exception | None = None
        for ml_service_url in ml_service_urls:
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    response = await client.post(
                        f"{ml_service_url}/analyze",
                        data={"inspection_id": str(inspection.id)},
                        files={
                            "image": (
                                file.filename or "inspection.jpg",
                                image_bytes,
                                file.content_type or "application/octet-stream",
                            )
                        },
                        headers={"X-ML-Service-Token": settings.ML_SERVICE_TOKEN},
                    )
                    response.raise_for_status()
                last_error = None
                break
            except httpx.HTTPError as exc:
                last_error = exc
                logger.warning(
                    "ML service call failed for inspection %s at %s: %s",
                    inspection.id,
                    ml_service_url,
                    exc,
                )

        if last_error is not None:
            logger.warning(
                "Inspection %s photo uploaded, but ML analysis could not be triggered",
                inspection.id,
            )

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


@router.patch("/{inspection_id}/analysis", response_model=AnalysisResponse)
async def patch_inspection_analysis(
    inspection_id: uuid.UUID,
    payload: AnalysisUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_or_ml_service),
):
    if current_user is None:
        return await inspection_service.update_inspection_analysis_internal(
            db,
            inspection_id,
            payload,
        )

    return await inspection_service.update_inspection_analysis(
        db,
        current_user.id,
        inspection_id,
        payload,
    )
