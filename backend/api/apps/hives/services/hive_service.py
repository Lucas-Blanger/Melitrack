import uuid
from datetime import datetime, timezone

from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.hives.models import Hive
from apps.hives.schemas import HiveCreate, HiveUpdate
from .common import get_owned_hive
from .photo_service import delete_photos_by_hive


async def create_hive(
    db: AsyncSession,
    owner_id: uuid.UUID,
    payload: HiveCreate,
) -> Hive:
    hive = Hive(owner_id=owner_id, **payload.model_dump())

    db.add(hive)
    await db.commit()
    await db.refresh(hive)

    return hive


async def list_hives(db: AsyncSession, owner_id: uuid.UUID) -> list[Hive]:
    result = await db.execute(
        select(Hive).where(Hive.owner_id == owner_id).order_by(Hive.created_at)
    )
    return list(result.scalars().all())


async def get_hive(
    db: AsyncSession,
    hive_id: uuid.UUID,
    owner_id: uuid.UUID,
) -> Hive:
    return await get_owned_hive(db, hive_id, owner_id)


async def update_hive(
    db: AsyncSession,
    hive_id: uuid.UUID,
    owner_id: uuid.UUID,
    payload: HiveUpdate,
) -> Hive:
    hive = await get_owned_hive(db, hive_id, owner_id)

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(hive, field, value)

    hive.updated_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(hive)

    return hive


async def delete_hive(
    db: AsyncSession,
    mongo: AsyncIOMotorDatabase,
    hive_id: uuid.UUID,
    owner_id: uuid.UUID,
) -> None:
    hive = await get_owned_hive(db, hive_id, owner_id)

    await delete_photos_by_hive(mongo, owner_id, hive.id)

    await db.delete(hive)
    await db.commit()
