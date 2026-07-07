from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    unit: str = Field(..., min_length=1, max_length=20)
    description: str | None = None


class ProductUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    unit: str | None = Field(None, min_length=1, max_length=20)
    description: str | None = None
    is_active: bool | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    unit: str
    description: str | None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
