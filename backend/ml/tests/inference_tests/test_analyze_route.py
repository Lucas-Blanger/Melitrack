import base64
from io import BytesIO
from types import SimpleNamespace

import pytest
from fastapi import HTTPException, UploadFile
from PIL import Image
from starlette.datastructures import Headers

from app.routes import analyze as analyze_route


def _image_bytes() -> bytes:
    buffer = BytesIO()
    Image.new("RGB", (8, 8), color=(120, 80, 40)).save(buffer, format="PNG")
    return buffer.getvalue()


def _upload_file(
    content: bytes,
    content_type: str = "image/png",
    filename: str = "hive.png",
) -> UploadFile:
    return UploadFile(
        filename=filename,
        file=BytesIO(content),
        headers=Headers({"content-type": content_type}),
    )


@pytest.mark.anyio
async def test_analyze_rejects_missing_token(monkeypatch):
    send_task = _mock_send_task(monkeypatch)

    with pytest.raises(HTTPException) as exc_info:
        await analyze_route.analyze(
            inspection_id="inspection-1",
            image=_upload_file(_image_bytes()),
            ml_service_token=None,
        )

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid internal token"
    send_task.assert_not_called()


@pytest.mark.anyio
async def test_analyze_rejects_invalid_token(monkeypatch):
    send_task = _mock_send_task(monkeypatch)

    with pytest.raises(HTTPException) as exc_info:
        await analyze_route.analyze(
            inspection_id="inspection-1",
            image=_upload_file(_image_bytes()),
            ml_service_token="wrong-token",
        )

    assert exc_info.value.status_code == 401
    send_task.assert_not_called()


@pytest.mark.anyio
async def test_analyze_rejects_non_image_file(monkeypatch):
    send_task = _mock_send_task(monkeypatch)

    with pytest.raises(HTTPException) as exc_info:
        await analyze_route.analyze(
            inspection_id="inspection-1",
            image=_upload_file(b"not an image", content_type="text/plain"),
            ml_service_token="test-ml-token",
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "File uploaded is not an image"
    send_task.assert_not_called()


@pytest.mark.anyio
async def test_analyze_rejects_empty_image(monkeypatch):
    send_task = _mock_send_task(monkeypatch)

    with pytest.raises(HTTPException) as exc_info:
        await analyze_route.analyze(
            inspection_id="inspection-1",
            image=_upload_file(b""),
            ml_service_token="test-ml-token",
        )

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Empty image"
    send_task.assert_not_called()


@pytest.mark.anyio
async def test_analyze_dispatches_celery_task_with_base64_image(monkeypatch):
    send_task = _mock_send_task(monkeypatch, task_id="task-123")
    image_bytes = _image_bytes()

    response = await analyze_route.analyze(
        inspection_id="inspection-1",
        image=_upload_file(image_bytes),
        ml_service_token="test-ml-token",
    )

    assert response == {
        "status": "accepted",
        "inspection_id": "inspection-1",
        "task_id": "task-123",
    }
    send_task.assert_called_once()

    _, kwargs = send_task.call_args
    assert kwargs["queue"] == "ml"
    assert kwargs["args"][0] == "inspection-1"
    assert base64.b64decode(kwargs["args"][1]) == image_bytes


def _mock_send_task(monkeypatch, task_id: str = "task-id"):
    from unittest.mock import Mock

    send_task = Mock(return_value=SimpleNamespace(id=task_id))
    monkeypatch.setattr(analyze_route.celery, "send_task", send_task)
    monkeypatch.setattr(analyze_route.settings, "ML_SERVICE_TOKEN", "test-ml-token")
    return send_task
