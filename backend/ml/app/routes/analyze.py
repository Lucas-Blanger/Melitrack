import base64
import secrets

from fastapi import APIRouter, File, Form, Header, HTTPException, UploadFile, status

from app.config import settings
from app.tasks.celery_app import celery

router = APIRouter()


@router.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def analyze(
    inspection_id: str = Form(...),
    image: UploadFile = File(...),
    ml_service_token: str | None = Header(default=None, alias="X-ML-Service-Token"),
):
    if not ml_service_token or not secrets.compare_digest(
        ml_service_token, settings.ML_SERVICE_TOKEN
    ):
        raise HTTPException(status_code=401, detail="Invalid internal token")

    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File uploaded is not an image")

    image_bytes = await image.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image")

    image_payload = base64.b64encode(image_bytes).decode("ascii")
    task = celery.send_task(
        "app.tasks.analysis_tasks.analyze_hive_photo",
        args=[inspection_id, image_payload],
        queue="ml",
    )
    return {"status": "accepted", "inspection_id": inspection_id, "task_id": task.id}
