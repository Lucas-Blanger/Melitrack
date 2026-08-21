import secrets

from fastapi import APIRouter, File, Header, HTTPException, UploadFile, status

from app.config import settings
from app.inference.species import SpeciesClassifier

router = APIRouter(prefix="/species")

_classifier_instance = None


def get_species_classifier() -> SpeciesClassifier:
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = SpeciesClassifier()
    return _classifier_instance


@router.post("/identify")
async def identify_species(
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

    return get_species_classifier().predict(image_bytes)
