import httpx
from fastapi import HTTPException, UploadFile, status

from apps.hives.schemas import SpeciesIdentificationResponse
from config import get_settings
from core.exceptions import BadRequestException


async def identify_species(file: UploadFile) -> SpeciesIdentificationResponse:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise BadRequestException("File uploaded is not an image")

    image_bytes = await file.read()
    if not image_bytes:
        raise BadRequestException("Empty image")

    settings = get_settings()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.ML_SERVICE_URL}/species/identify",
                files={
                    "image": (
                        file.filename or "bee.jpg",
                        image_bytes,
                        file.content_type,
                    )
                },
                headers={"X-ML-Service-Token": settings.ML_SERVICE_TOKEN},
            )
            response.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML species service unavailable",
        ) from exc

    return SpeciesIdentificationResponse.model_validate(response.json())
