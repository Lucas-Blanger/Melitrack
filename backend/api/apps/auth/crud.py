from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserRegister, UserUpdate
from core.logger import get_logger

logger = get_logger()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: UserRegister) -> User:
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        hashed_password=user_in.password,
    )
    db.add(new_user)

    try:
        await db.commit()
        await db.refresh(new_user)
    except IntegrityError:
        logger.exception("Failed to create user due to IntegrityError")
        await db.rollback()
        raise

    return new_user


async def update_user(
    db: AsyncSession, user_id: str, user_in: UserUpdate
) -> User | None:
    user = await get_user_by_id(db, user_id)
    if not user:
        return None

    update_data = user_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError:
        logger.exception("Failed to update user due to IntegrityError")
        await db.rollback()
        raise

    return user


async def delete_user(db: AsyncSession, user_id: str) -> bool:
    user = await get_user_by_id(db, user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True
