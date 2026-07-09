from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from apps.auth.routes import router as auth_router
from apps.health_service.routes.health_routes import router as health_router
from apps.hives.routes import router as hives_router
from core.logger import get_logger

logger = get_logger(__name__)
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
app.include_router(hives_router)
