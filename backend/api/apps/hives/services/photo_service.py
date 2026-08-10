import uuid
from base64 import b64encode
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import UploadFile
from motor.motor_asyncio import AsyncIOMotorDatabase

from core.exceptions import BadRequestError, NotFoundError
from apps.hives.models import AnalysisStatus
from apps.hives.schemas import PhotoResponse

MAX_PHOTO_SIZE = 10 * 1024 * 1024


async def read_image(file: UploadFile) -> bytes:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise BadRequestError("Upload an image file")

    content = await file.read()

    if not content:
        raise BadRequestError("Empty file")

    if len(content) > MAX_PHOTO_SIZE:
        raise BadRequestError("Image larger than 10MB")

    return content


def serialize_photo(doc: dict) -> PhotoResponse:
    data_url = None
    if doc.get("data"):
        encoded = b64encode(doc["data"]).decode("ascii")
        data_url = f"data:{doc['content_type']};base64,{encoded}"

    return PhotoResponse(
        id=str(doc["_id"]),
        filename=doc["filename"],
        content_type=doc["content_type"],
        size=doc["size"],
        uploaded_at=doc["uploaded_at"],
        data_url=data_url,
    )


async def list_hive_photos(
    mongo: AsyncIOMotorDatabase,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
) -> list[PhotoResponse]:
    docs = await (
        mongo.hive_photos.find(
            {
                "owner_id": str(owner_id),
                "hive_id": str(hive_id),
            }
        )
        .sort("uploaded_at", -1)
        .to_list(length=10)
    )
    return [serialize_photo(doc) for doc in docs]


async def upload_hive_photo(
    mongo: AsyncIOMotorDatabase,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
    file: UploadFile,
) -> PhotoResponse:
    content = await read_image(file)
    uploaded_at = datetime.now(timezone.utc)

    result = await mongo.hive_photos.insert_one(
        {
            "owner_id": str(owner_id),
            "hive_id": str(hive_id),
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "data": content,
            "uploaded_at": uploaded_at,
        }
    )

    doc = await mongo.hive_photos.find_one({"_id": result.inserted_id})
    return serialize_photo(doc)


async def delete_hive_photo(
    mongo: AsyncIOMotorDatabase,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
    photo_id: str,
) -> None:
    if not ObjectId.is_valid(photo_id):
        raise NotFoundError("Photo not found")

    result = await mongo.hive_photos.delete_one(
        {
            "_id": ObjectId(photo_id),
            "owner_id": str(owner_id),
            "hive_id": str(hive_id),
        }
    )

    if result.deleted_count == 0:
        raise NotFoundError("Photo not found")


async def upload_inspection_photo(
    mongo: AsyncIOMotorDatabase,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
    inspection_id: uuid.UUID,
    file: UploadFile,
) -> PhotoResponse:
    content = await read_image(file)
    uploaded_at = datetime.now(timezone.utc)

    result = await mongo.inspection_photos.insert_one(
        {
            "owner_id": str(owner_id),
            "hive_id": str(hive_id),
            "inspection_id": str(inspection_id),
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "data": content,
            "uploaded_at": uploaded_at,
            "ml_status": AnalysisStatus.pending.value,
        }
    )

    doc = await mongo.inspection_photos.find_one({"_id": result.inserted_id})
    return serialize_photo(doc)


async def delete_photos_by_hive(
    mongo: AsyncIOMotorDatabase,
    owner_id: uuid.UUID,
    hive_id: uuid.UUID,
) -> None:
    await mongo.hive_photos.delete_many(
        {"owner_id": str(owner_id), "hive_id": str(hive_id)}
    )
    await mongo.inspection_photos.delete_many(
        {"owner_id": str(owner_id), "hive_id": str(hive_id)}
    )
