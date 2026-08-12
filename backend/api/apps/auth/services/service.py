from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from core.exceptions import BadRequestError, UnauthorizedError
from core.logger import get_logger
from core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from .. import crud
from .email_service import EmailService
from ..models import User
from ..schemas import UserLogin, UserRegister, UserUpdate
from ..utils import generate_reset_code, hash_reset_code

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

        # User created via Google does not have a password.
        if not user.hashed_password:
            logger.warning("Authentication failed: user has no password configured")
            raise UnauthorizedError(detail="This account uses Google authentication")

        if not verify_password(
            login_data.password,
            user.hashed_password,
        ):
            logger.warning("Authentication failed: invalid password")
            raise UnauthorizedError()

        logger.info("User authenticated: %s", login_data.email)

        return user

    @staticmethod
    async def authenticate_google(
        db: AsyncSession,
        user_info: dict,
    ) -> User:

        google_id = user_info["sub"]

        user = await crud.get_user_by_google_id(
            db,
            google_id,
        )

        if user:
            user.picture = user_info.get("picture", getattr(user, "picture", ""))
            user.auth_provider = "google"
            await db.commit()
            await db.refresh(user)
            return user

        user = await crud.get_user_by_email(
            db,
            user_info["email"],
        )

        if user:
            user.google_id = google_id
            user.picture = user_info.get("picture", user.picture)
            user.auth_provider = "google"

            await db.commit()
            await db.refresh(user)

            return user

        return await crud.create_google_user(
            db=db,
            google_id=google_id,
            name=user_info["name"],
            email=user_info["email"],
            picture=user_info.get("picture", ""),
        )

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

    @staticmethod
    async def update_user_settings(
        db: AsyncSession,
        user: User,
        user_data: UserUpdate,
    ) -> User:
        if user_data.email and user_data.email != user.email:
            existing_user = await crud.get_user_by_email(db, user_data.email)
            if existing_user and existing_user.id != user.id:
                raise BadRequestError(detail="Email already registered")

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            await db.commit()
            await db.refresh(user)
        except IntegrityError as exc:
            await db.rollback()
            raise BadRequestError(detail="Email already registered") from exc

        return user

    @staticmethod
    async def change_password(
        db: AsyncSession,
        user: User,
        current_password: str,
        new_password: str,
        confirm_password: str,
    ) -> None:
        if user.auth_provider == "google" or not user.hashed_password:
            raise BadRequestError("Contas autenticadas via Google não possuem senha local")

        if not verify_password(current_password, user.hashed_password):
            raise BadRequestError("Senha atual incorreta")

        if new_password != confirm_password:
            raise BadRequestError("A nova senha e a confirmação não coincidem")

        await crud.update_password(
            db=db,
            user=user,
            hashed_password=get_password_hash(new_password),
        )
