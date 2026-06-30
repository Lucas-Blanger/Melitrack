import pytest
from datetime import datetime
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_register():
    fake_user = SimpleNamespace(
        id="1",
        name="Lucas",
        email="lucas@email.com",
        is_active=True,
        created_at=datetime.utcnow(),
    )

    with patch(
        "apps.auth.routes.AuthService.register_user",
        new=AsyncMock(return_value=fake_user),
    ):
        response = client.post(
            "/auth/register",
            json={
                "name": "Lucas",
                "email": "lucas@email.com",
                "password": "12345678",
            },
        )

    assert response.status_code == 201

    body = response.json()

    assert body["id"] == "1"
    assert body["name"] == "Lucas"
    assert body["email"] == "lucas@email.com"
    assert body["is_active"] is True


def test_login():
    fake_user = SimpleNamespace(
        id="123",
        email="lucas@email.com",
    )

    with patch(
        "apps.auth.routes.AuthService.authenticate_user",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.routes.AuthService.create_token",
        return_value="fake-jwt-token",
    ):

        response = client.post(
            "/auth/login",
            json={
                "email": "lucas@email.com",
                "password": "12345678",
            },
        )

    assert response.status_code == 200

    body = response.json()

    assert body["access_token"] == "fake-jwt-token"

    assert "session" in response.cookies
    assert response.cookies["session"] == "fake-jwt-token"


def test_logout():
    response = client.post("/auth/logout")

    assert response.status_code == 200

    assert response.json() == {"message": "Logged out successfully"}
