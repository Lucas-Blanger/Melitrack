import pytest
from unittest.mock import AsyncMock, patch
from core.exceptions import BadRequestError, UnauthorizedError

from apps.auth.service import AuthService

from apps.auth.schemas import UserRegister, UserLogin


@pytest.mark.asyncio
async def test_register_user_success():
    db = AsyncMock()

    user_data = UserRegister(
        name="Lucas",
        email="lucas@email.com",
        password="12345678",
    )

    with patch(
        "apps.auth.service.crud.get_user_by_email",
        new=AsyncMock(return_value=None),
    ), patch(
        "apps.auth.service.get_password_hash",
        return_value="hashed_password",
    ), patch(
        "apps.auth.service.crud.create_user",
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
        "apps.auth.service.crud.get_user_by_email",
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
        "apps.auth.service.crud.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.service.verify_password",
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
        "apps.auth.service.crud.get_user_by_email",
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
        "apps.auth.service.crud.get_user_by_email",
        new=AsyncMock(return_value=fake_user),
    ), patch(
        "apps.auth.service.verify_password",
        return_value=False,
    ):
        with pytest.raises(UnauthorizedError):
            await AuthService.authenticate_user(db, login)


def test_create_token():
    with patch(
        "apps.auth.service.create_access_token",
        return_value="fake-token",
    ):

        token = AuthService.create_token("123")

        assert token == "fake-token"
