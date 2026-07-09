import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from apps.hives.services.common import (
    get_owned_hive,
    get_owned_inspection,
)
from core.exceptions import ForbiddenError, NotFoundError


@pytest.mark.asyncio
async def test_get_owned_hive_success():
    owner_id = uuid.uuid4()

    hive = SimpleNamespace(
        id=uuid.uuid4(),
        owner_id=owner_id,
    )

    db = AsyncMock()
    db.get.return_value = hive

    result = await get_owned_hive(
        db,
        hive.id,
        owner_id,
    )

    assert result == hive


@pytest.mark.asyncio
async def test_get_owned_hive_not_found():
    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError):
        await get_owned_hive(
            db,
            uuid.uuid4(),
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_get_owned_hive_forbidden():
    hive = SimpleNamespace(
        id=uuid.uuid4(),
        owner_id=uuid.uuid4(),
    )

    db = AsyncMock()
    db.get.return_value = hive

    with pytest.raises(ForbiddenError):
        await get_owned_hive(
            db,
            hive.id,
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_get_owned_inspection_success():
    owner_id = uuid.uuid4()

    inspection = SimpleNamespace(
        id=uuid.uuid4(),
        owner_id=owner_id,
    )

    db = AsyncMock()
    db.get.return_value = inspection

    result = await get_owned_inspection(
        db,
        inspection.id,
        owner_id,
    )

    assert result == inspection


@pytest.mark.asyncio
async def test_get_owned_inspection_not_found():
    db = AsyncMock()
    db.get.return_value = None

    with pytest.raises(NotFoundError):
        await get_owned_inspection(
            db,
            uuid.uuid4(),
            uuid.uuid4(),
        )


@pytest.mark.asyncio
async def test_get_owned_inspection_forbidden():
    inspection = SimpleNamespace(
        id=uuid.uuid4(),
        owner_id=uuid.uuid4(),
    )

    db = AsyncMock()
    db.get.return_value = inspection

    with pytest.raises(ForbiddenError):
        await get_owned_inspection(
            db,
            inspection.id,
            uuid.uuid4(),
        )
