import uuid

import pytest
from unittest.mock import AsyncMock, Mock

from apps.hives.services import dashboard_service


@pytest.mark.asyncio
async def test_get_dashboard_overview():
    db = AsyncMock()

    owner_id = uuid.uuid4()

    count_result = Mock()
    count_result.scalar_one.return_value = 5

    inspection = {
        "id": str(uuid.uuid4()),
        "hive_id": str(uuid.uuid4()),
        "owner_id": str(uuid.uuid4()),
        "health": "excelente",
        "notes": "ok",
        "inspected_at": "2024-01-01T00:00:00Z",
    }

    inspection_result = Mock()
    inspection_result.scalars.return_value.first.return_value = inspection

    alert_result = Mock()
    alert_result.scalar_one.return_value = 2

    db.execute.side_effect = [
        count_result,
        inspection_result,
        alert_result,
    ]

    result = await dashboard_service.get_dashboard_overview(
        db,
        owner_id,
    )

    assert result.total_hives == 5
    assert result.last_inspection is not None
    assert result.last_inspection.health == "excelente"
    assert result.health_alerts == 2
