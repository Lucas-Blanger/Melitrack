from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


Enjoyment = Literal["gostando", "neutro", "nao_gostando"]


class FeedbackCreate(BaseModel):
    enjoyment: Enjoyment
    comments: str = Field(..., min_length=3, max_length=3000)
    suggestions: str | None = Field(None, max_length=3000)

    @field_validator("comments")
    @classmethod
    def validate_comments(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("Conte um pouco sobre sua experiência.")
        return value

    @field_validator("suggestions")
    @classmethod
    def clean_suggestions(cls, value: str | None) -> str | None:
        value = value.strip() if value else None
        return value or None


class FeedbackResponseSchema(BaseModel):
    id: UUID
    enjoyment: Enjoyment
    comments: str
    suggestions: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
