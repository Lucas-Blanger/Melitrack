from io import BytesIO
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import HTTPException, UploadFile
from starlette.datastructures import Headers

from apps.hives.services import species_service


def _upload_file(content: bytes, content_type: str = "image/png") -> UploadFile:
    return UploadFile(
        filename="bee.png",
        file=BytesIO(content),
        headers=Headers({"content-type": content_type}),
    )


@pytest.mark.asyncio
async def test_identify_species_rejects_non_image():
    with pytest.raises(HTTPException) as exc_info:
        await species_service.identify_species(_upload_file(b"txt", "text/plain"))

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_identify_species_calls_ml_service():
    response = Mock()
    response.json.return_value = {
        "prediction": {
            "label": "Jataí",
            "scientific_name": "Tetragonisca angustula",
            "confidence": 0.72,
        },
        "alternatives": [
            {
                "label": "Mirim",
                "scientific_name": "Plebeia spp.",
                "confidence": 0.18,
            }
        ],
    }
    response.raise_for_status.return_value = None

    client = AsyncMock()
    client.post.return_value = response

    with patch("apps.hives.services.species_service.httpx.AsyncClient") as client_cls:
        client_cls.return_value.__aenter__.return_value = client

        result = await species_service.identify_species(_upload_file(b"image"))

    assert result.prediction.label == "Jataí"
    client.post.assert_awaited_once()
