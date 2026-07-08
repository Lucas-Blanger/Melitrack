import uuid
from datetime import date, datetime, time, timezone

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.hives.models import Harvest, Product
from apps.hives.schemas import (
    HarvestCreate,
    HarvestSummaryItem,
    HarvestSummaryResponse,
)
from core.exceptions import NotFoundError
from .common import get_owned_hive


async def create_harvest(
    db: AsyncSession,
    owner_id: uuid.UUID,
    payload: HarvestCreate,
) -> Harvest:
    await get_owned_hive(db, payload.hive_id, owner_id)

    product = await db.get(Product, payload.product_id)

    if not product:
        raise NotFoundError("Product not found")

    data = payload.model_dump()

    data["owner_id"] = owner_id
    data["unit"] = payload.unit or product.unit
    data["harvested_at"] = payload.harvested_at or datetime.now(timezone.utc)

    data.pop("product_id")

    harvest = Harvest(
        **data,
        product=product,
    )

    db.add(harvest)
    await db.commit()
    await db.refresh(harvest)

    return harvest


async def list_harvests_by_hive(
    db: AsyncSession,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
) -> list[Harvest]:
    await get_owned_hive(db, hive_id, owner_id)

    result = await db.execute(
        select(Harvest)
        .where(Harvest.hive_id == hive_id, Harvest.owner_id == owner_id)
        .order_by(desc(Harvest.harvested_at))
    )

    return list(result.scalars().all())


async def get_harvest_summary(
    db: AsyncSession,
    owner_id: uuid.UUID,
    start_date: date | None = None,
    end_date: date | None = None,
) -> HarvestSummaryResponse:
    query = (
        select(
            Product.name.label("product"),
            Harvest.unit,
            func.sum(Harvest.quantity).label("total_quantity"),
        )
        .join(
            Product,
            Harvest.product_id == Product.id,
        )
        .where(Harvest.owner_id == owner_id)
    )

    if start_date:
        query = query.where(
            Harvest.harvested_at >= datetime.combine(start_date, time.min)
        )

    if end_date:
        query = query.where(
            Harvest.harvested_at <= datetime.combine(end_date, time.max)
        )

    query = query.group_by(
        Product.name,
        Harvest.unit,
    ).order_by(Product.name)

    result = await db.execute(query)

    return HarvestSummaryResponse(
        period_start=start_date,
        period_end=end_date,
        items=[
            HarvestSummaryItem(
                product=row.product,
                unit=row.unit,
                total_quantity=float(row.total_quantity or 0),
            )
            for row in result
        ],
    )
