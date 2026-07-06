import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import TYPE_CHECKING

from sqlalchemy import String, Float, DateTime, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base

if TYPE_CHECKING:
    from apps.hives.models.inspection import Inspection
    from apps.hives.models.harvest import Harvest
from apps.hives.models.enums import HiveType


class Hive(Base):
    __tablename__ = "hives"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    type: Mapped[HiveType] = mapped_column(Enum(HiveType), nullable=False)
    species: Mapped[str] = mapped_column(String(100), nullable=False)  # ex: "Jataí"

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    location_description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    photos: Mapped[list["HivePhoto"]] = relationship(
        back_populates="hive", cascade="all, delete-orphan"
    )
    inspections: Mapped[list["Inspection"]] = relationship(
        back_populates="hive", cascade="all, delete-orphan"
    )
    harvests: Mapped[list["Harvest"]] = relationship(
        back_populates="hive", cascade="all, delete-orphan"
    )


class HivePhoto(Base):
    __tablename__ = "hive_photos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    hive_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("hives.id"), nullable=False)

    url: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hive: Mapped["Hive"] = relationship(back_populates="photos")
