import uuid
from unittest.mock import AsyncMock, Mock, patch

import pytest

from apps.hives.models import ColonyHealth, Inspection
from apps.hives.schemas import InspectionCreate
from apps.hives.services import inspection_service


@pytest.mark.asyncio
async def test_create_inspection():
    db = Mock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.add = Mock()

    owner_id = uuid.uuid4()
    hive_id = uuid.uuid4()

    payload = InspectionCreate(
        hive_id=hive_id,
        health=ColonyHealth.excellent,
        queen_seen=True,
        honey_level=80,
        population_estimate="Alta",
        notes="Tudo bem",
    )

    with patch(
        "apps.hives.services.inspection_service.get_owned_hive",
        new=AsyncMock(),
    ):
        inspection = await inspection_service.create_inspection(db, owner_id, payload)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert inspection.owner_id == owner_id
    assert inspection.hive_id == hive_id
    assert inspection.health == payload.health
    assert inspection.queen_seen is True
    assert inspection.honey_level == 80
    assert inspection.population_estimate == "Alta"
    assert inspection.notes == "Tudo bem"


@pytest.mark.asyncio
async def test_list_inspections_by_hive():
    db = AsyncMock()
    owner_id = uuid.uuid4()
    hive_id = uuid.uuid4()

    expected_inspections = [Mock(), Mock()]
    result = Mock()
    result.scalars.return_value.all.return_value = expected_inspections
    db.execute.return_value = result

    with patch(
        "apps.hives.services.inspection_service.get_owned_hive",
        new=AsyncMock(),
    ):
        inspections = await inspection_service.list_inspections_by_hive(
            db, owner_id, hive_id
        )

    db.execute.assert_awaited_once()
    assert inspections == expected_inspections


@pytest.mark.asyncio
async def test_get_inspection():
    db = AsyncMock()
    owner_id = uuid.uuid4()
    inspection_id = uuid.uuid4()
    expected_inspection = Mock()

    with patch(
        "apps.hives.services.inspection_service.get_owned_inspection",
        new=AsyncMock(return_value=expected_inspection),
    ) as get_owned_inspection_mock:
        inspection = await inspection_service.get_inspection(
            db, owner_id, inspection_id
        )

    get_owned_inspection_mock.assert_awaited_once_with(db, inspection_id, owner_id)
    assert inspection is expected_inspection
