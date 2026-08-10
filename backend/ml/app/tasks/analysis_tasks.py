import base64
import logging

import httpx
from app.tasks.celery_app import celery
from app.inference.pipeline import get_pipeline
from app.config import settings

logger = logging.getLogger(__name__)
MODEL_NAME = "EfficientNetB0-v1"


def _send_callback(inspection_id: str, payload: dict) -> None:
    url = f"{settings.HIVE_SERVICE_URL}/inspections/{inspection_id}/analysis"
    headers = {"X-ML-Service-Token": settings.ML_SERVICE_TOKEN}
    with httpx.Client(timeout=15) as client:
        response = client.patch(url, json=payload, headers=headers)
        response.raise_for_status()


def _confidence(result: dict) -> float:
    anomaly_scores = result["anomaly"]["scores"].values()
    population_score = result["population"]["density_score"]
    scores = [float(score) for score in anomaly_scores] + [float(population_score)]
    return round(sum(scores) / len(scores), 4)


@celery.task(
    name="app.tasks.analysis_tasks.analyze_hive_photo",
    queue="ml",
    bind=True,
    max_retries=3,
)
def analyze_hive_photo(self, inspection_id: str, image_payload: str):
    try:
        image_bytes = base64.b64decode(image_payload)
        pipeline = get_pipeline()
        result = pipeline.run(image_bytes)
        payload = {
            "status": "processed",
            "model_name": MODEL_NAME,
            "result": result,
            "confidence": _confidence(result),
        }
        _send_callback(inspection_id, payload)
        return {"status": "processed", "inspection_id": inspection_id}
    except Exception as exc:
        error_message = str(exc)
        failed_payload = {"status": "failed", "error_message": error_message}

        try:
            _send_callback(inspection_id, failed_payload)
        except Exception as callback_exc:
            logger.warning(
                "Failed to send failure callback for inspection %s: %s",
                inspection_id,
                callback_exc,
            )

        if self.request.retries >= self.max_retries:
            logger.exception(
                "Analysis failed permanently for inspection %s", inspection_id
            )
            raise

        raise self.retry(exc=exc, countdown=60)
