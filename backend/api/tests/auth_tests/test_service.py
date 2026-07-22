from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from core.exceptions import BadRequestError, UnauthorizedError

from apps.auth.schemas import UserLogin, UserRegister
from apps.auth.services.service import AuthService


@pytest.mark.asyncio
async def test_register_user_success():
    db = AsyncMock()

    user_data = UserRegister(
        name="Lucas",
        email="lucas@email.com",
        password="12345678",
    )

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=None),
    ), patch(
        "apps.auth.services.service.get_password_hash",
        return_value="hashed_password",
    ), patch(
        "apps.auth.services.service.crud.create_user",
        new=AsyncMock(),
    ) as create_user:

        await AuthService.register_user(db, user_data)

        create_user.assert_called_once()


@pytest.mark.asyncio
async def test_register_existing_email():
    db = AsyncMock()

    user_data = UserRegister(
        name="Lucas",
        email="lucas@email.com",
        password="12345678",
    )

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=object()),
    ):
        with pytest.raises(BadRequestError):
            await AuthService.register_user(db, user_data)


@pytest.mark.asyncio
async def test_authenticate_success():
    db = AsyncMock()

    login = UserLogin(
        email="lucas@email.com",
        password="12345678",
    )

    fake_user = type(
        "User",
        (),
        {
            "hashed_password": "hash",
            "email": login.email,
        },
    )

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.services.service.verify_password",
        return_value=True,
    ):

        user = await AuthService.authenticate_user(db, login)

        assert user.email == login.email


@pytest.mark.asyncio
async def test_login_user_not_found():
    db = AsyncMock()

    login = UserLogin(
        email="abc@email.com",
        password="12345678",
    )

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=None),
    ):
        with pytest.raises(UnauthorizedError):
            await AuthService.authenticate_user(db, login)


@pytest.mark.asyncio
async def test_login_invalid_password():
    db = AsyncMock()

    login = UserLogin(
        email="abc@email.com",
        password="12345678",
    )

    fake_user = type(
        "User",
        (),
        {
            "hashed_password": "hash",
        },
    )

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.services.service.verify_password",
        return_value=False,
    ):
        with pytest.raises(UnauthorizedError):
            await AuthService.authenticate_user(db, login)


def test_create_token():
    with patch(
        "apps.auth.services.service.create_access_token",
        return_value="fake-token",
    ):

        token = AuthService.create_token("123")

        assert token == "fake-token"


@pytest.mark.asyncio
async def test_forgot_password_sends_reset_code():
    db = AsyncMock()
    user = SimpleNamespace(email="lucas@email.com")

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=user),
    ), patch(
        "apps.auth.services.service.generate_reset_code",
        return_value="123456",
    ), patch(
        "apps.auth.services.service.hash_reset_code",
        return_value="hashed-code",
    ), patch(
        "apps.auth.services.service.crud.save_reset_code",
        new=AsyncMock(),
    ) as save_reset_code, patch(
        "apps.auth.services.service.EmailService.send_reset_code",
        new=AsyncMock(),
    ) as send_reset_code:
        await AuthService.forgot_password(db, "lucas@email.com")

    save_reset_code.assert_awaited_once()
    send_reset_code.assert_awaited_once_with("lucas@email.com", "123456")


@pytest.mark.asyncio
async def test_verify_reset_code_success():
    db = AsyncMock()
    fake_user = SimpleNamespace(
        reset_code="hashed-code",
        reset_code_expires=datetime.now(timezone.utc) + timedelta(minutes=10),
    )

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.services.service.hash_reset_code",
        return_value="hashed-code",
    ):
        await AuthService.verify_reset_code(db, "lucas@email.com", "123456")


@pytest.mark.asyncio
async def test_reset_password_updates_password():
    db = AsyncMock()
    fake_user = SimpleNamespace(email="lucas@email.com")

    with patch.object(
        AuthService,
        "verify_reset_code",
        new=AsyncMock(),
    ), patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.services.service.get_password_hash",
        return_value="new-hash",
    ), patch(
        "apps.auth.services.service.crud.update_password",
        new=AsyncMock(),
    ) as update_password:
        await AuthService.reset_password(
            db,
            "lucas@email.com",
            "123456",
            "new-password",
            "new-password",
        )

    update_password.assert_awaited_once()


@pytest.mark.asyncio
async def test_google_auth_new_user():
    db = AsyncMock()

    google_user = {
        "sub": "google-123",
        "google_id": "google-123",
        "email": "lucas@gmail.com",
        "name": "Lucas",
        "picture": "https://picture.com/avatar.png",
    }

    with patch(
        "apps.auth.services.service.crud.get_user_by_google_id",
        new=AsyncMock(return_value=None),
    ), patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=None),
    ), patch(
        "apps.auth.services.service.crud.create_google_user",
        new=AsyncMock(),
    ) as create_google_user:

        await AuthService.authenticate_google(
            db,
            google_user,
        )

    create_google_user.assert_called_once()


@pytest.mark.asyncio
async def test_google_auth_existing_user():
    db = AsyncMock()

    fake_user = SimpleNamespace(
        id="123",
        email="lucas@gmail.com",
        google_id="google-123",
    )

    google_user = {
        "sub": "google-123",
        "google_id": "google-123",
        "email": "lucas@gmail.com",
        "name": "Lucas",
        "picture": "avatar.png",
    }

    with patch(
        "apps.auth.services.service.crud.get_user_by_google_id",
        new=AsyncMock(return_value=fake_user),
    ):

        user = await AuthService.authenticate_google(
            db,
            google_user,
        )

    assert user.google_id == "google-123"
