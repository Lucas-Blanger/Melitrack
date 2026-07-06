import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from apps.hives.models import ColonyHealth


class InspectionCreate(BaseModel):
    hive_id: uuid.UUID
    health: ColonyHealth
    queen_seen: bool | None = None
    honey_level: int | None = Field(None, ge=0, le=100)
    population_estimate: str | None = Field(None, max_length=50)
    notes: str | None = None
    inspected_at: datetime | None = None


class InspectionResponse(InspectionCreate):
    id: uuid.UUID
    owner_id: uuid.UUID
    inspected_at: datetime

    model_config = ConfigDict(from_attributes=True)
