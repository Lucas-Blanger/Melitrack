from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from apps.hives.routes import dashboard as dashboard_routes
from main import app

client = TestClient(app)


def fake_user():
    return SimpleNamespace(id=uuid4())


def test_get_dashboard_overview():
    fake_dashboard = SimpleNamespace(
        total_hives=8,
        last_inspection=SimpleNamespace(
            id=str(uuid4()),
            hive_id=str(uuid4()),
            owner_id=str(uuid4()),
            inspected_at=datetime.now(timezone.utc),
            notes="Tudo certo",
            health="excelente",
        ),
        health_alerts=1,
    )

    app.dependency_overrides[dashboard_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.dashboard.dashboard_service.get_dashboard_overview",
            new=AsyncMock(return_value=fake_dashboard),
        ):
            response = client.get("/dashboard/overview")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200

    body = response.json()

    assert body["total_hives"] == 8
    assert body["health_alerts"] == 1
