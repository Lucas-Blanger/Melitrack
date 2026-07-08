import uuid
from datetime import datetime, timezone

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.hives.models import AnalysisStatus, Inspection, MLPrediction
from apps.hives.schemas import AnalysisResponse, InspectionCreate
from .common import get_owned_hive, get_owned_inspection


async def create_inspection(
    db: AsyncSession,
    owner_id: uuid.UUID,
    payload: InspectionCreate,
) -> Inspection:
    await get_owned_hive(db, payload.hive_id, owner_id)

    data = payload.model_dump()
    data["owner_id"] = owner_id
    data["inspected_at"] = payload.inspected_at or datetime.now(timezone.utc)

    inspection = Inspection(**data)

    db.add(inspection)
    await db.commit()
    await db.refresh(inspection)

    return inspection


async def list_inspections_by_hive(
    db: AsyncSession,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
) -> list[Inspection]:
    await get_owned_hive(db, hive_id, owner_id)

    result = await db.execute(
        select(Inspection)
        .where(Inspection.hive_id == hive_id, Inspection.owner_id == owner_id)
        .order_by(desc(Inspection.inspected_at))
    )

    return list(result.scalars().all())


async def get_inspection(
    db: AsyncSession,
    owner_id: uuid.UUID,
    inspection_id: uuid.UUID,
) -> Inspection:
    return await get_owned_inspection(db, inspection_id, owner_id)


async def ensure_pending_analysis(
    db: AsyncSession,
    inspection_id: uuid.UUID,
) -> None:
    result = await db.execute(
        select(MLPrediction).where(MLPrediction.inspection_id == inspection_id)
    )

    if result.scalars().first():
        return

    db.add(
        MLPrediction(
            inspection_id=inspection_id,
            status=AnalysisStatus.pending,
        )
    )
    await db.commit()


async def get_inspection_analysis(
    db: AsyncSession,
    owner_id: uuid.UUID,
    inspection_id: uuid.UUID,
) -> AnalysisResponse:
    inspection = await get_owned_inspection(db, inspection_id, owner_id)

    result = await db.execute(
        select(MLPrediction).where(MLPrediction.inspection_id == inspection.id)
    )
    prediction = result.scalars().first()

    if not prediction:
        return AnalysisResponse(status=AnalysisStatus.pending)

    return AnalysisResponse(
        status=prediction.status,
        model_name=prediction.model_name,
        result=prediction.result,
        confidence=prediction.confidence,
        error_message=prediction.error_message,
        processed_at=prediction.processed_at,
    )
