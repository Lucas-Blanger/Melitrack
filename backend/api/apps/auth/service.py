from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from core.security import get_password_hash, verify_password, create_access_token
from core.exceptions import BadRequestError, UnauthorizedError
from .models import User
from .schemas import UserRegister, UserLogin
from . import crud


class AuthService:

    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserRegister) -> User:
        # Check if user already exists
        existing_user = await crud.get_user_by_email(db, user_data.email)
        if existing_user:
            raise BadRequestError(detail="Email already registered")

        # Hash password
        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password

        # Create user
        user = await crud.create_user(db, user_data)
        return user

    @staticmethod
    async def authenticate_user(db: AsyncSession, login_data: UserLogin) -> User:
        # Get user by email
        user = await crud.get_user_by_email(db, login_data.email)
        if not user:
            raise UnauthorizedError()

        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedError()

        return user

    @staticmethod
    def create_token(user_id: str, expires_delta: timedelta | None = None) -> str:
        return create_access_token(
            data={"sub": str(user_id)}, expires_delta=expires_delta
        )
