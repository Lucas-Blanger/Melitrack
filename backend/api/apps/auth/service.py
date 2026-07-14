from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import BadRequestError, UnauthorizedError
from core.logger import get_logger
from core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from . import crud
from .email_service import EmailService
from .models import User
from .schemas import UserLogin, UserRegister
from .utils import generate_reset_code, hash_reset_code

logger = get_logger(__name__)


class AuthService:

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
        logger.info("Registering user: %s", user_data.email)

        existing_user = await crud.get_user_by_email(db, user_data.email)
        if existing_user:
            logger.warning(
                "Registration failed: email %s already exists",
                user_data.email,
            )
            raise BadRequestError(detail="Email already registered")

        user_data.password = get_password_hash(user_data.password)

        user = await crud.create_user(db, user_data)

        logger.info("User registered: %s", user_data.email)

        return user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession,
        login_data: UserLogin,
    ) -> User:
        logger.info("Login attempt for %s", login_data.email)

        user = await crud.get_user_by_email(db, login_data.email)

        if not user:
            logger.warning("Authentication failed: user not found")
            raise UnauthorizedError()

        if not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            logger.warning("Authentication failed: invalid password")
            raise UnauthorizedError()

        logger.info("User authenticated: %s", login_data.email)

        return user

    @staticmethod
    def create_token(
        user_id: str,
        expires_delta: timedelta | None = None,
    ) -> str:
        logger.info("Creating access token for user: %s", user_id)

        return create_access_token(
            data={"sub": str(user_id)},
            expires_delta=expires_delta,
        )

    @staticmethod
    async def forgot_password(
        db: AsyncSession,
        email: str,
    ) -> None:

        user = await crud.get_user_by_email(db, email)

        if not user:
            return

        code = generate_reset_code()

        await crud.save_reset_code(
            db=db,
            user=user,
            code_hash=hash_reset_code(code),
            expires=datetime.now(timezone.utc) + timedelta(minutes=10),
        )

        await EmailService.send_reset_code(
            user.email,
            code,
        )

    @staticmethod
    async def verify_reset_code(
        db: AsyncSession,
        email: str,
        code: str,
    ) -> None:

        user = await crud.get_user_by_email(db, email)

        if not user:
            raise BadRequestError("Invalid code")

        if user.reset_code != hash_reset_code(code):
            raise BadRequestError("Invalid code")

        if (
            user.reset_code_expires is None
            or datetime.now(timezone.utc) > user.reset_code_expires
        ):
            raise BadRequestError("Code expired")

    @staticmethod
    async def reset_password(
        db: AsyncSession,
        email: str,
        code: str,
        new_password: str,
        confirm_password: str,
    ) -> None:

        if new_password != confirm_password:
            raise BadRequestError("Passwords do not match")

        await AuthService.verify_reset_code(
            db=db,
            email=email,
            code=code,
        )

        user = await crud.get_user_by_email(db, email)

        await crud.update_password(
            db=db,
            user=user,
            hashed_password=get_password_hash(new_password),
        )
