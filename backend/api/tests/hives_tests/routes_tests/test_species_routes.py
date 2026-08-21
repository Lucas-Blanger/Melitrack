from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from fastapi.testclient import TestClient

from apps.hives.routes import species as species_routes
from main import app

client = TestClient(app)


def fake_user():
    return SimpleNamespace(id=uuid4())


def test_identify_species():
    result = {
        "prediction": {
            "label": "Jataí",
            "scientific_name": "Tetragonisca angustula",
            "confidence": 0.72,
        },
        "alternatives": [],
    }

    app.dependency_overrides[species_routes.get_current_user] = lambda: fake_user()

    try:
        with patch(
            "apps.hives.routes.species.species_service.identify_species",
            new=AsyncMock(return_value=result),
        ):
            response = client.post(
                "/species/identify",
                files={"image": ("bee.png", b"fake-image", "image/png")},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["prediction"]["label"] == "Jataí"
