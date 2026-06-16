from fastapi import FastAPI

from apps.health_service.routes.health_routes import router as health_router

app = FastAPI()
app.include_router(health_router)
