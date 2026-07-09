import uuid
from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock, patch, MagicMock

import pytest

from apps.hives.models import Hive, HiveType
from apps.hives.schemas import HiveCreate, HiveUpdate
from apps.hives.services import hive_service


@pytest.mark.asyncio
async def test_create_hive():
    db = Mock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    db.add = Mock()

    owner_id = uuid.uuid4()

    payload = HiveCreate(
        name="Colmeia 1",
        type=HiveType.box,
        species="Jataí",
        latitude=-22.0,
        longitude=-47.0,
        location_description="Quintal",
        notes="OK",
    )

    hive = await hive_service.create_hive(db, owner_id, payload)

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert hive.owner_id == owner_id
    assert hive.name == payload.name
    assert hive.type == payload.type
    assert hive.species == payload.species
    assert hive.latitude == payload.latitude
    assert hive.longitude == payload.longitude


@pytest.mark.asyncio
async def test_list_hives():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    owner_id = uuid.uuid4()

    expected_hives = [Mock(), Mock()]
    result = Mock()
    result.scalars.return_value.all.return_value = expected_hives
    db.execute.return_value = result

    hives = await hive_service.list_hives(db, owner_id)

    db.execute.assert_awaited_once()
    assert hives == expected_hives


@pytest.mark.asyncio
async def test_get_hive():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    owner_id = uuid.uuid4()
    hive_id = uuid.uuid4()
    expected_hive = Mock()

    with patch(
        "apps.hives.services.hive_service.get_owned_hive",
        new=AsyncMock(return_value=expected_hive),
    ) as get_owned_hive_mock:
        hive = await hive_service.get_hive(db, hive_id, owner_id)

    get_owned_hive_mock.assert_awaited_once_with(db, hive_id, owner_id)
    assert hive is expected_hive


@pytest.mark.asyncio
async def test_update_hive():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()
    owner_id = uuid.uuid4()
    hive_id = uuid.uuid4()

    hive = Hive(
        owner_id=owner_id,
        name="Antiga",
        type=HiveType.box,
        species="Jataí",
    )
    hive.updated_at = datetime(2024, 1, 1, tzinfo=timezone.utc)

    payload = HiveUpdate(
        name="Nova",
        species="Africanizada",
        latitude=-21.5,
        longitude=-48.5,
    )

    with patch(
        "apps.hives.services.hive_service.get_owned_hive",
        new=AsyncMock(return_value=hive),
    ):
        updated_hive = await hive_service.update_hive(db, hive_id, owner_id, payload)

    assert updated_hive.name == "Nova"
    assert updated_hive.species == "Africanizada"
    assert updated_hive.latitude == -21.5
    assert updated_hive.longitude == -48.5
    assert updated_hive.updated_at >= datetime(2024, 1, 1, tzinfo=timezone.utc)
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(updated_hive)


@pytest.mark.asyncio
async def test_delete_hive():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    mongo = object()
    owner_id = uuid.uuid4()
    hive_id = uuid.uuid4()

    hive = Hive(
        owner_id=owner_id,
        name="Para remover",
        type=HiveType.trap,
        species="Jataí",
    )
    hive.id = hive_id

    with patch(
        "apps.hives.services.hive_service.get_owned_hive",
        new=AsyncMock(return_value=hive),
    ) as get_owned_hive_mock, patch(
        "apps.hives.services.hive_service.delete_photos_by_hive",
        new=AsyncMock(),
    ) as delete_photos_mock:
        await hive_service.delete_hive(db, mongo, hive_id, owner_id)

    get_owned_hive_mock.assert_awaited_once_with(db, hive_id, owner_id)
    delete_photos_mock.assert_awaited_once_with(mongo, owner_id, hive_id)
    db.delete.assert_called_once_with(hive)
    db.commit.assert_awaited_once()
