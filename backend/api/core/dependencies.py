from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_async_session_local


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async_session_local = get_async_session_local()
    async with async_session_local() as session:
        yield session
