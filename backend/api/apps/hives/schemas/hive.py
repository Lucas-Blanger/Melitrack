import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from apps.hives.models import HiveType


class HiveCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    type: HiveType
    species: str = Field(..., min_length=1, max_length=100)
    latitude: float | None = None
    longitude: float | None = None
    location_description: str | None = Field(None, max_length=255)
    notes: str | None = None


class HiveUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    type: HiveType | None = None
    species: str | None = Field(None, min_length=1, max_length=100)
    latitude: float | None = None
    longitude: float | None = None
    location_description: str | None = Field(None, max_length=255)
    notes: str | None = None


class HiveResponse(HiveCreate):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
