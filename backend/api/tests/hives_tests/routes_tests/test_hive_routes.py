from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from apps.hives.routes import hives as hives_routes
from main import app

client = TestClient(app)


def fake_user():
    return SimpleNamespace(id=uuid4())


def test_create_hive():
    fake_hive = SimpleNamespace(
        id=str(uuid4()),
        owner_id=str(uuid4()),
        name="Colmeia 1",
        type="caixa",
        species="Apis mellifera",
        latitude=-27.1,
        longitude=-52.1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[hives_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.hives.hive_service.create_hive",
            new=AsyncMock(return_value=fake_hive),
        ):
            response = client.post(
                "/hives",
                json={
                    "name": "Colmeia 1",
                    "type": "caixa",
                    "species": "Apis mellifera",
                    "latitude": -27.1,
                    "longitude": -52.1,
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201

    body = response.json()

    assert body["name"] == "Colmeia 1"


def test_list_hives():
    fake_hive = SimpleNamespace(
        id=str(uuid4()),
        owner_id=str(uuid4()),
        name="Colmeia 1",
        type="caixa",
        species="Apis mellifera",
        latitude=-27.1,
        longitude=-52.1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[hives_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.hives.hive_service.list_hives",
            new=AsyncMock(return_value=[fake_hive]),
        ):
            response = client.get("/hives")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_hive():
    fake_hive = SimpleNamespace(
        id=str(uuid4()),
        owner_id=str(uuid4()),
        name="Colmeia 1",
        type="caixa",
        species="Apis mellifera",
        latitude=-27.1,
        longitude=-52.1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[hives_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.hives.hive_service.get_hive",
            new=AsyncMock(return_value=fake_hive),
        ):
            response = client.get(f"/hives/{fake_hive.id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["name"] == "Colmeia 1"


def test_update_hive():
    fake_hive = SimpleNamespace(
        id=str(uuid4()),
        owner_id=str(uuid4()),
        name="Colmeia Atualizada",
        type="caixa",
        species="Apis mellifera",
        latitude=-27.1,
        longitude=-52.1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[hives_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.hives.hive_service.update_hive",
            new=AsyncMock(return_value=fake_hive),
        ):
            response = client.put(
                f"/hives/{fake_hive.id}",
                json={
                    "name": "Colmeia Atualizada",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["name"] == "Colmeia Atualizada"


def test_delete_hive():
    hive_id = str(uuid4())

    app.dependency_overrides[hives_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.hives.hive_service.delete_hive",
            new=AsyncMock(),
        ):
            response = client.delete(f"/hives/{hive_id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 204
