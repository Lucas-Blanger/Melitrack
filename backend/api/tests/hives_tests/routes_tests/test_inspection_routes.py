import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from apps.hives.routes import inspections as inspections_routes
from main import app

client = TestClient(app)


def fake_user():
    return SimpleNamespace(id=uuid.uuid4())


def fake_inspection():
    return SimpleNamespace(
        id=uuid.uuid4(),
        hive_id=uuid.uuid4(),
        owner_id=uuid.uuid4(),
        inspected_at=datetime.now(timezone.utc),
        notes="Inspection",
        health="excelente",
    )


def test_create_inspection():
    inspection = fake_inspection()

    app.dependency_overrides[inspections_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.inspections.inspection_service.create_inspection",
            new=AsyncMock(return_value=inspection),
        ):
            response = client.post(
                "/inspections",
                json={
                    "hive_id": str(inspection.hive_id),
                    "health": "excelente",
                    "notes": "Inspection",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201


def test_list_inspections():
    inspection = fake_inspection()

    app.dependency_overrides[inspections_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.inspections.inspection_service.list_inspections_by_hive",
            new=AsyncMock(return_value=[inspection]),
        ):
            response = client.get(f"/inspections/hive/{inspection.hive_id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_inspection():
    inspection = fake_inspection()

    app.dependency_overrides[inspections_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.inspections.inspection_service.get_inspection",
            new=AsyncMock(return_value=inspection),
        ):
            response = client.get(f"/inspections/{inspection.id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
