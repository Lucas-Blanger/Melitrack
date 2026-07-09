from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_product():
    fake_product = SimpleNamespace(
        id=1,
        name="Mel",
        unit="kg",
        description="Mel puro",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    with patch(
        "apps.hives.routes.product.product_service.create_product",
        new=AsyncMock(return_value=fake_product),
    ):
        response = client.post(
            "/products",
            json={
                "name": "Mel",
                "unit": "kg",
                "description": "Mel puro",
            },
        )

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == 1
    assert body["name"] == "Mel"


def test_list_products():
    fake_products = [
        SimpleNamespace(
            id=1,
            name="Mel",
            unit="kg",
            description="Mel",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
    ]

    with patch(
        "apps.hives.routes.product.product_service.list_products",
        new=AsyncMock(return_value=fake_products),
    ):
        response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 1
