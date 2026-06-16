from fastapi import APIRouter
from datetime import datetime, UTC

router = APIRouter(prefix="/health", tags=["Health Check"])


@router.get("/")
def health_check():
    return {"status": "ok", "timestamp": datetime.now(UTC).isoformat()}
