import uuid

from sqlalchemy import desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.hives.models import ColonyHealth, Hive, Inspection
from apps.hives.schemas import DashboardOverview


async def get_dashboard_overview(
    db: AsyncSession,
    owner_id: uuid.UUID,
) -> DashboardOverview:
    total_hives_result = await db.execute(
        select(func.count()).select_from(Hive).where(Hive.owner_id == owner_id)
    )

    last_inspection_result = await db.execute(
        select(Inspection)
        .where(Inspection.owner_id == owner_id)
        .order_by(desc(Inspection.inspected_at))
        .limit(1)
    )

    alerts_result = await db.execute(
        select(func.count())
        .select_from(Inspection)
        .where(
            Inspection.owner_id == owner_id,
            Inspection.health.in_([ColonyHealth.poor, ColonyHealth.critical]),
        )
    )

    return DashboardOverview(
        total_hives=total_hives_result.scalar_one(),
        last_inspection=last_inspection_result.scalars().first(),
        health_alerts=alerts_result.scalar_one(),
    )
