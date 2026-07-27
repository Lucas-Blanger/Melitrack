from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.health import app as health_router

app = FastAPI(title="Melitrack ML Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)
app.include_router(health_router)
