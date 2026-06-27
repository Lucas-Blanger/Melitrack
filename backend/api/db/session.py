from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from config import get_settings

settings = get_settings()
database_url = settings.get_database_url()

engine = create_async_engine(database_url, future=True, echo=settings.DEBUG)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
