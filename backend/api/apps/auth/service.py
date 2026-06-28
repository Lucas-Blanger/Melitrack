from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash, verify_password, create_access_token
from core.exceptions import BadRequestError, UnauthorizedError
from core.logger import get_logger
from .models import User
from .schemas import UserRegister, UserLogin
from . import crud

logger = get_logger()


class AuthService:

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
        logger.info("Registering user: %s", user_data.email)
        # Check if user already exists
        existing_user = await crud.get_user_by_email(db, user_data.email)
        if existing_user:
            logger.warning(
                "Registration failed: email %s already exists", user_data.email
            )
            raise BadRequestError(detail="Email already registered")

        # Hash password
        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password

        # Create user
        user = await crud.create_user(db, user_data)
        logger.info("User registered: %s", user_data.email)
        return user

    @staticmethod
    async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> User:
        logger.info("Login attempt for %s", login_data.email)
        # Get user by email
        user = await crud.get_user_by_email(db, login_data.email)
        if not user:
            logger.warning("Authentication failed: user not found")
            raise UnauthorizedError()

        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            logger.warning("Authentication failed: invalid password")
            raise UnauthorizedError()

        logger.info("User authenticated: %s", login_data.email)
        return user

    @staticmethod
    def create_token(user_id: str, expires_delta: timedelta | None = None) -> str:
        logger.info("Creating access token for user: %s", user_id)
        return create_access_token(
            data={"sub": str(user_id)}, expires_delta=expires_delta
        )
