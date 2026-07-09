import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock, patch

import pytest

from apps.hives.models import AnalysisStatus, ColonyHealth, Inspection, MLPrediction
from apps.hives.schemas import AnalysisResponse, InspectionCreate
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


@pytest.mark.asyncio
async def test_ensure_pending_analysis_creates_prediction():
    db = Mock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.add = Mock()

    inspection_id = uuid.uuid4()

    result = Mock()
    result.scalars.return_value.first.return_value = None
    db.execute.return_value = result

    await inspection_service.ensure_pending_analysis(db, inspection_id)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    assert isinstance(db.add.call_args[0][0], MLPrediction)
    assert db.add.call_args[0][0].inspection_id == inspection_id
    assert db.add.call_args[0][0].status == AnalysisStatus.pending


@pytest.mark.asyncio
async def test_ensure_pending_analysis_skips_existing_prediction():
    db = Mock()
    db.execute = AsyncMock()
    db.commit = AsyncMock()
    db.add = Mock()

    inspection_id = uuid.uuid4()

    result = Mock()
    result.scalars.return_value.first.return_value = Mock()
    db.execute.return_value = result

    await inspection_service.ensure_pending_analysis(db, inspection_id)

    db.add.assert_not_called()
    db.commit.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_inspection_analysis_returns_pending_when_missing():
    db = AsyncMock()
    owner_id = uuid.uuid4()
    inspection_id = uuid.uuid4()

    inspection = Inspection(
        owner_id=owner_id,
        hive_id=uuid.uuid4(),
        health=ColonyHealth.good,
    )
    inspection.id = inspection_id

    result = Mock()
    result.scalars.return_value.first.return_value = None

    db.execute.return_value = result

    with patch(
        "apps.hives.services.inspection_service.get_owned_inspection",
        new=AsyncMock(return_value=inspection),
    ):
        analysis = await inspection_service.get_inspection_analysis(
            db, owner_id, inspection_id
        )

    assert isinstance(analysis, AnalysisResponse)
    assert analysis.status == AnalysisStatus.pending


@pytest.mark.asyncio
async def test_get_inspection_analysis_returns_existing_prediction():
    db = AsyncMock()
    owner_id = uuid.uuid4()
    inspection_id = uuid.uuid4()

    inspection = Inspection(
        owner_id=owner_id,
        hive_id=uuid.uuid4(),
        health=ColonyHealth.good,
    )
    inspection.id = inspection_id

    prediction = MLPrediction(
        inspection_id=inspection_id,
        status=AnalysisStatus.processed,
        model_name="modelo-x",
        result={"label": "saudável"},
        confidence=0.91,
        error_message=None,
        processed_at=datetime(2024, 1, 1, tzinfo=timezone.utc),
    )

    result = Mock()
    result.scalars.return_value.first.return_value = prediction

    db.execute.return_value = result

    with patch(
        "apps.hives.services.inspection_service.get_owned_inspection",
        new=AsyncMock(return_value=inspection),
    ):
        analysis = await inspection_service.get_inspection_analysis(
            db, owner_id, inspection_id
        )

    assert analysis.status == AnalysisStatus.processed
    assert analysis.model_name == "modelo-x"
    assert analysis.result == {"label": "saudável"}
    assert analysis.confidence == 0.91
    assert analysis.error_message is None
    assert analysis.processed_at == datetime(2024, 1, 1, tzinfo=timezone.utc)
