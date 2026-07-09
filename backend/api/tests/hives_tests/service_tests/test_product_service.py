import pytest

from unittest.mock import AsyncMock, patch, MagicMock

from apps.hives.schemas import ProductCreate, ProductUpdate
from apps.hives.services import product_service


@pytest.mark.asyncio
async def test_create_product():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    payload = ProductCreate(
        name="Mel",
        unit="kg",
        description="Mel puro",
    )

    product = await product_service.create_product(
        db,
        payload,
    )

    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()

    assert product.name == "Mel"


@pytest.mark.asyncio
async def test_get_product():
    db = AsyncMock()

    fake_product = object()

    db.get.return_value = fake_product

    result = await product_service.get_product(
        db,
        1,
    )

    assert result == fake_product


@pytest.mark.asyncio
async def test_update_product():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    fake_product = type(
        "Product",
        (),
        {
            "name": "Mel",
            "unit": "kg",
        },
    )()

    payload = ProductUpdate(
        name="Própolis",
    )

    with patch(
        "apps.hives.services.product_service.get_product",
        new=AsyncMock(return_value=fake_product),
    ):
        result = await product_service.update_product(
            db,
            1,
            payload,
        )

    assert result.name == "Própolis"

    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_product():
    db = AsyncMock()
    db.add = MagicMock()
    db.commit = AsyncMock()
    db.refresh = AsyncMock()

    fake_product = type(
        "Product",
        (),
        {
            "is_active": True,
        },
    )()

    with patch(
        "apps.hives.services.product_service.get_product",
        new=AsyncMock(return_value=fake_product),
    ):
        await product_service.delete_product(
            db,
            1,
        )

    assert fake_product.is_active is False

    db.commit.assert_awaited_once()
