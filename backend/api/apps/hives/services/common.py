import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import ForbiddenError, NotFoundError
from apps.hives.models import Hive, Inspection


async def get_owned_hive(
    db: AsyncSession,
    hive_id: uuid.UUID,
    owner_id: uuid.UUID,
) -> Hive:
    hive = await db.get(Hive, hive_id)

    if not hive:
        raise NotFoundError("Hive not found")

    if hive.owner_id != owner_id:
        raise ForbiddenError("You do not have permission to access this hive")

    return hive


async def get_owned_inspection(
    db: AsyncSession,
    inspection_id: uuid.UUID,
    owner_id: uuid.UUID,
) -> Inspection:
    inspection = await db.get(Inspection, inspection_id)

    if not inspection:
        raise NotFoundError("Inspection not found")

    if inspection.owner_id != owner_id:
        raise ForbiddenError("You do not have permission to access this inspection")

    return inspection
