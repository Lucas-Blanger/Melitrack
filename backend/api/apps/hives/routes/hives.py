import uuid

from fastapi import APIRouter, Depends, File, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth.models import User
from apps.hives.schemas import HiveCreate, HiveResponse, HiveUpdate, PhotoResponse
from apps.hives.services import hive_service, photo_service
from apps.hives.services.common import get_owned_hive
from core.dependencies import get_current_user, get_db, get_mongo_db

router = APIRouter(prefix="/hives", tags=["hives"])


@router.post("", response_model=HiveResponse, status_code=status.HTTP_201_CREATED)
async def create_hive(
    payload: HiveCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await hive_service.create_hive(db, current_user.id, payload)


@router.get("", response_model=list[HiveResponse])
async def list_hives(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await hive_service.list_hives(db, current_user.id)


@router.get("/{hive_id}", response_model=HiveResponse)
async def get_hive(
    hive_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await hive_service.get_hive(db, hive_id, current_user.id)


@router.put("/{hive_id}", response_model=HiveResponse)
async def update_hive(
    hive_id: uuid.UUID,
    payload: HiveUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await hive_service.update_hive(db, hive_id, current_user.id, payload)


@router.delete("/{hive_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hive(
    hive_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db),
    current_user: User = Depends(get_current_user),
):
    await hive_service.delete_hive(db, mongo, hive_id, current_user.id)


@router.post(
    "/{hive_id}/photos",
    response_model=PhotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_hive_photo(
    hive_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db),
    current_user: User = Depends(get_current_user),
):
    hive = await get_owned_hive(db, hive_id, current_user.id)
    return await photo_service.upload_hive_photo(mongo, current_user.id, hive.id, file)


@router.delete("/{hive_id}/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hive_photo(
    hive_id: uuid.UUID,
    photo_id: str,
    db: AsyncSession = Depends(get_db),
    mongo: AsyncIOMotorDatabase = Depends(get_mongo_db),
    current_user: User = Depends(get_current_user),
):
    await get_owned_hive(db, hive_id, current_user.id)
    await photo_service.delete_hive_photo(mongo, current_user.id, hive_id, photo_id)
