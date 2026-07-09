from datetime import datetime, timezone
from io import BytesIO
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import UploadFile
from starlette.datastructures import Headers

from apps.hives.services.photo_service import (
    MAX_PHOTO_SIZE,
    delete_hive_photo,
    delete_photos_by_hive,
    read_image,
    serialize_photo,
    upload_hive_photo,
    upload_inspection_photo,
)
from core.exceptions import BadRequestError, NotFoundError


@pytest.mark.asyncio
async def test_read_image_success():
    file = UploadFile(
        filename="photo.jpg",
        file=BytesIO(b"image"),
        headers=Headers({"content-type": "image/jpeg"}),
    )

    content = await read_image(file)

    assert content == b"image"


@pytest.mark.asyncio
async def test_read_image_invalid_content_type():
    file = UploadFile(
        filename="file.txt",
        file=BytesIO(b"text"),
        headers=Headers({"content-type": "text/plain"}),
    )

    with pytest.raises(BadRequestError):
        await read_image(file)


@pytest.mark.asyncio
async def test_read_image_empty():
    file = UploadFile(
        filename="photo.jpg",
        file=BytesIO(b""),
        headers=Headers({"content-type": "image/jpeg"}),
    )

    with pytest.raises(BadRequestError):
        await read_image(file)


@pytest.mark.asyncio
async def test_read_image_too_large():
    file = UploadFile(
        filename="photo.jpg",
        file=BytesIO(b"a" * (MAX_PHOTO_SIZE + 1)),
        headers=Headers({"content-type": "image/jpeg"}),
    )

    with pytest.raises(BadRequestError):
        await read_image(file)


def test_serialize_photo():
    now = datetime.now(timezone.utc)

    doc = {
        "_id": "abc123",
        "filename": "photo.jpg",
        "content_type": "image/jpeg",
        "size": 123,
        "uploaded_at": now,
    }

    photo = serialize_photo(doc)

    assert photo.id == "abc123"
    assert photo.filename == "photo.jpg"
    assert photo.content_type == "image/jpeg"
    assert photo.size == 123
    assert photo.uploaded_at == now


@pytest.mark.asyncio
async def test_delete_hive_photo_invalid_object_id():
    mongo = AsyncMock()

    with pytest.raises(NotFoundError):
        await delete_hive_photo(
            mongo,
            "owner",
            "hive",
            "invalid-id",
        )


@pytest.mark.asyncio
async def test_delete_hive_photo_not_found():
    mongo = AsyncMock()

    mongo.hive_photos.delete_one = AsyncMock(
        return_value=SimpleNamespace(
            deleted_count=0,
        )
    )

    with pytest.raises(NotFoundError):
        await delete_hive_photo(
            mongo,
            "owner",
            "hive",
            "507f1f77bcf86cd799439011",
        )


@pytest.mark.asyncio
async def test_delete_hive_photo_success():
    mongo = AsyncMock()

    mongo.hive_photos.delete_one = AsyncMock(
        return_value=SimpleNamespace(
            deleted_count=1,
        )
    )

    await delete_hive_photo(
        mongo,
        "owner",
        "hive",
        "507f1f77bcf86cd799439011",
    )

    mongo.hive_photos.delete_one.assert_called_once()


@pytest.mark.asyncio
async def test_delete_photos_by_hive():
    mongo = AsyncMock()

    mongo.hive_photos.delete_many = AsyncMock()
    mongo.inspection_photos.delete_many = AsyncMock()

    await delete_photos_by_hive(
        mongo,
        "owner",
        "hive",
    )

    mongo.hive_photos.delete_many.assert_called_once()
    mongo.inspection_photos.delete_many.assert_called_once()


@pytest.mark.asyncio
async def test_upload_hive_photo():
    mongo = AsyncMock()

    mongo.hive_photos.insert_one = AsyncMock(
        return_value=SimpleNamespace(inserted_id="1")
    )

    mongo.hive_photos.find_one = AsyncMock(
        return_value={
            "_id": "1",
            "filename": "photo.jpg",
            "content_type": "image/jpeg",
            "size": 5,
            "uploaded_at": datetime.now(timezone.utc),
        }
    )

    file = UploadFile(
        filename="photo.jpg",
        file=BytesIO(b"image"),
    )
    file._content_type = "image/jpeg"

    with patch(
        "apps.hives.services.photo_service.read_image",
        new=AsyncMock(return_value=b"image"),
    ):
        photo = await upload_hive_photo(
            mongo,
            "owner",
            "hive",
            file,
        )

    assert photo.filename == "photo.jpg"


@pytest.mark.asyncio
async def test_upload_inspection_photo():
    mongo = AsyncMock()

    mongo.inspection_photos.insert_one = AsyncMock(
        return_value=SimpleNamespace(inserted_id="1")
    )

    mongo.inspection_photos.find_one = AsyncMock(
        return_value={
            "_id": "1",
            "filename": "photo.jpg",
            "content_type": "image/jpeg",
            "size": 5,
            "uploaded_at": datetime.now(timezone.utc),
        }
    )

    file = UploadFile(
        filename="photo.jpg",
        file=BytesIO(b"image"),
    )
    file._content_type = "image/jpeg"

    with patch(
        "apps.hives.services.photo_service.read_image",
        new=AsyncMock(return_value=b"image"),
    ):
        photo = await upload_inspection_photo(
            mongo,
            "owner",
            "hive",
            "inspection",
            file,
        )

    assert photo.filename == "photo.jpg"
