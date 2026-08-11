import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import httpx

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


def test_get_analysis():
    analysis = SimpleNamespace(
        status="pending",
        model_name=None,
        result=None,
        confidence=None,
        error_message=None,
        processed_at=None,
    )

    app.dependency_overrides[inspections_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.inspections.inspection_service.get_inspection_analysis",
            new=AsyncMock(return_value=analysis),
        ):
            response = client.get(f"/inspections/{uuid.uuid4()}/analysis")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_patch_analysis():
    analysis = SimpleNamespace(
        status="processed",
        model_name="EfficientNetB0-v1",
        result={"population": {"density_score": 0.9}},
        confidence=0.8,
        error_message=None,
        processed_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[inspections_routes.get_current_user_or_ml_service] = (
        lambda: fake_user()
    )

    try:
        with patch(
            "apps.hives.routes.inspections.inspection_service.update_inspection_analysis",
            new=AsyncMock(return_value=analysis),
        ):
            response = client.patch(
                f"/inspections/{uuid.uuid4()}/analysis",
                json={
                    "status": "processed",
                    "model_name": "EfficientNetB0-v1",
                    "result": {"population": {"density_score": 0.9}},
                    "confidence": 0.8,
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200


def test_upload_photo_does_not_fail_when_ml_service_is_unreachable():
    inspection = fake_inspection()
    photo = SimpleNamespace(
        id=str(uuid.uuid4()),
        filename="photo.jpg",
        content_type="image/jpeg",
        size=11,
        uploaded_at=datetime.now(timezone.utc),
    )

    app.dependency_overrides[inspections_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.inspections.inspection_service.get_inspection",
            new=AsyncMock(return_value=inspection),
        ), patch(
            "apps.hives.routes.inspections.photo_service.upload_inspection_photo",
            new=AsyncMock(return_value=photo),
        ), patch(
            "apps.hives.routes.inspections.inspection_service.ensure_pending_analysis",
            new=AsyncMock(return_value=None),
        ), patch(
            "apps.hives.routes.inspections.httpx.AsyncClient",
            side_effect=httpx.ConnectError("temporary failure"),
        ):
            response = client.post(
                f"/inspections/{inspection.id}/photos",
                files={"file": ("photo.jpg", b"fake-image", "image/jpeg")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 201
    assert response.json()["id"] == photo.id
