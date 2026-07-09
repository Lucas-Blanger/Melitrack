import uuid

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from apps.hives.models import Product
from apps.hives.schemas import HarvestCreate
from apps.hives.services import harvest_service
from core.exceptions import NotFoundError


@pytest.mark.asyncio
async def test_create_harvest():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    owner_id = uuid.uuid4()
    hive_id = uuid.uuid4()

    product = Product(id=1, name="Mel", unit="kg")

    db.get.return_value = product

    payload = HarvestCreate(
        hive_id=hive_id,
        product_id=1,
        quantity=3,
        quality_notes="Teste",
    )

    with patch(
        "apps.hives.services.harvest_service.get_owned_hive",
        new=AsyncMock(),
    ):
        harvest = await harvest_service.create_harvest(
            db,
            owner_id,
            payload,
        )

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert harvest.quantity == 3
    assert harvest.unit == "kg"


@pytest.mark.asyncio
async def test_create_harvest_product_not_found():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    owner_id = uuid.uuid4()

    db.get.return_value = None

    payload = HarvestCreate(
        hive_id=uuid.uuid4(),
        product_id=1,
        quantity=1,
    )

    with patch(
        "apps.hives.services.harvest_service.get_owned_hive",
        new=AsyncMock(),
    ):
        with pytest.raises(NotFoundError):
            await harvest_service.create_harvest(
                db,
                owner_id,
                payload,
            )


@pytest.mark.asyncio
async def test_list_harvests_by_hive():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    result = type(
        "Result",
        (),
        {
            "scalars": lambda self: type(
                "Scalars",
                (),
                {"all": lambda self: ["harvest"]},
            )(),
        },
    )()

    db.execute.return_value = result

    with patch(
        "apps.hives.services.harvest_service.get_owned_hive",
        new=AsyncMock(),
    ):
        harvests = await harvest_service.list_harvests_by_hive(
            db,
            uuid.uuid4(),
            uuid.uuid4(),
        )

    assert harvests == ["harvest"]


@pytest.mark.asyncio
async def test_get_harvest_summary():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    row = type(
        "Row",
        (),
        {
            "product": "Mel",
            "unit": "kg",
            "total_quantity": 20,
        },
    )

    db.execute.return_value = [row]

    result = await harvest_service.get_harvest_summary(
        db,
        uuid.uuid4(),
    )

    assert len(result.items) == 1
    assert result.items[0].product == "Mel"
    assert result.items[0].unit == "kg"
    assert result.items[0].total_quantity == 20
