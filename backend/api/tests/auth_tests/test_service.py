from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from core.exceptions import BadRequestError, UnauthorizedError

from apps.auth.schemas import UserLogin, UserRegister, UserUpdate
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
async def test_update_user_settings_updates_profile_and_preferences():
    db = AsyncMock()
    user = SimpleNamespace(
        id="123",
        name="Lucas",
        email="lucas@email.com",
        meliponary_name="Antigo",
        meliponary_location=None,
        inspection_frequency_days=14,
        notify_health_alerts=True,
        notify_email=True,
    )
    user_data = UserUpdate(
        name="Lucas Silva",
        email="lucas@email.com",
        meliponary_name="Meliponário Central",
        meliponary_location="Curitiba",
        inspection_frequency_days=21,
        notify_health_alerts=False,
        notify_email=False,
    )

    updated_user = await AuthService.update_user_settings(db, user, user_data)

    assert updated_user.name == "Lucas Silva"
    assert updated_user.meliponary_name == "Meliponário Central"
    assert updated_user.meliponary_location == "Curitiba"
    assert updated_user.inspection_frequency_days == 21
    assert updated_user.notify_health_alerts is False
    assert updated_user.notify_email is False
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once_with(user)


@pytest.mark.asyncio
async def test_update_user_settings_rejects_duplicate_email():
    db = AsyncMock()
    user = SimpleNamespace(id="123", email="lucas@email.com")
    existing_user = SimpleNamespace(id="456", email="outro@email.com")
    user_data = UserUpdate(email="outro@email.com")

    with patch(
        "apps.auth.services.service.crud.get_user_by_email",
        new=AsyncMock(return_value=existing_user),
    ):
        with pytest.raises(BadRequestError):
            await AuthService.update_user_settings(db, user, user_data)

    db.commit.assert_not_awaited()
