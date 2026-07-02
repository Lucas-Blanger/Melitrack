from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Request
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase

from db.session import get_async_session_local

from apps.auth import crud as auth_crud
from apps.auth.models import User
from core.exceptions import UnauthorizedError
from core.security import decode_access_token
from db.mongo import get_mongo_database
from db.session import get_async_session_local


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session_local = get_async_session_local()
    async with async_session_local() as session:
        yield session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session_local = get_async_session_local()
    async with async_session_local() as session:
        yield session


def get_mongo_db() -> AsyncIOMotorDatabase:
    return get_mongo_database()


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    token = request.cookies.get("session")

    authorization = request.headers.get("Authorization")
    if not token and authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]

    if not token:
        raise UnauthorizedError("Unauthenticated user")

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    except JWTError:
        raise UnauthorizedError("Invalid token")

    if not user_id:
        raise UnauthorizedError("Invalid token")

    user = await auth_crud.get_user_by_id(db, user_id)
    if not user or not user.is_active:
        raise UnauthorizedError("Invalid user or inactive")

    return user
