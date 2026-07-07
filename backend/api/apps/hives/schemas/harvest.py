import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from apps.hives.models import HarvestProduct


class HarvestCreate(BaseModel):
    hive_id: uuid.UUID
    product_id: int
    quantity: float = Field(..., gt=0)
    unit: str | None = Field(None, max_length=20)
    quality_notes: str | None = None
    harvested_at: datetime | None = None


class HarvestResponse(HarvestCreate):
    id: uuid.UUID
    owner_id: uuid.UUID
    unit: str
    harvested_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HarvestSummaryItem(BaseModel):
    product_id: int
    unit: str
    total_quantity: float


class HarvestSummaryResponse(BaseModel):
    period_start: date | None = None
    period_end: date | None = None
    items: list[HarvestSummaryItem]
