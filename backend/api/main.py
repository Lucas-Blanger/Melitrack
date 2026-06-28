from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from db.session import engine
from db.base import Base
from apps.auth.routes import router as auth_router
from apps.health_service.routes.health_routes import router as health_router
from core.logger import get_logger

logger = get_logger()
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(health_router)


@app.on_event("startup")
async def on_startup():
    logger.info("Starting application")
    # Initialize database on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialized successfully")
