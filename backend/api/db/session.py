from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_settings

engine = None
AsyncSessionLocal = None


def _get_settings():
    return get_settings()


def get_engine():
    global engine
    if engine is None:
        settings = _get_settings()
        database_url = settings.get_database_url()
        engine = create_async_engine(database_url, future=True, echo=settings.DEBUG)
    return engine


def get_async_session_local():
    global AsyncSessionLocal
    if AsyncSessionLocal is None:
        AsyncSessionLocal = sessionmaker(
            get_engine(), class_=AsyncSession, expire_on_commit=False
        )
    return AsyncSessionLocal
