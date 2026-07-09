from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from apps.hives.routes import harvests as harvests_routes
from main import app

client = TestClient(app)


def fake_user():
    return SimpleNamespace(id=uuid4())


def test_create_harvest():
    fake_harvest = SimpleNamespace(
        id=str(uuid4()),
        hive_id=str(uuid4()),
        owner_id=str(uuid4()),
        product_id=1,
        quantity=2.5,
        unit="kg",
        quality_notes="Excellent quality honey",
        harvested_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[harvests_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.harvests.harvest_service.create_harvest",
            new=AsyncMock(return_value=fake_harvest),
        ):
            response = client.post(
                "/harvests",
                json={
                    "hive_id": str(fake_harvest.hive_id),
                    "product_id": 1,
                    "quantity": 2.5,
                    "quality_notes": "Excellent quality honey",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201

    body = response.json()

    assert body["product_id"] == 1
    assert body["quantity"] == 2.5
    assert body["unit"] == "kg"


def test_list_harvests_by_hive():
    fake_harvest = SimpleNamespace(
        id=str(uuid4()),
        hive_id=str(uuid4()),
        owner_id=str(uuid4()),
        product_id=1,
        quantity=2.5,
        unit="kg",
        quality_notes=None,
        harvested_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[harvests_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.harvests.harvest_service.list_harvests_by_hive",
            new=AsyncMock(return_value=[fake_harvest]),
        ):
            response = client.get(f"/harvests/hive/{fake_harvest.hive_id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    body = response.json()

    assert len(body) == 1
    assert body[0]["product_id"] == 1


def test_get_harvest_summary():
    fake_summary = SimpleNamespace(
        period_start=None,
        period_end=None,
        items=[
            {
                "product": "Mel",
                "unit": "kg",
                "total_quantity": 15.5,
            }
        ],
    )

    app.dependency_overrides[harvests_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.harvests.harvest_service.get_harvest_summary",
            new=AsyncMock(return_value=fake_summary),
        ):
            response = client.get("/harvests/summary")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    body = response.json()

    assert body["items"][0]["product"] == "Mel"
    assert body["items"][0]["total_quantity"] == 15.5
