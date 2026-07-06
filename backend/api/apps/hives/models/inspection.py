import uuid
from datetime import datetime
from typing import TYPE_CHECKING


from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Float, Text, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship


from db.base import Base

if TYPE_CHECKING:
    from apps.hives.models.hive import Hive
from apps.hives.models.enums import ColonyHealth


class Inspection(Base):
    __tablename__ = "inspections"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    hive_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hives.id"), nullable=False, index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, index=True
    )

    health: Mapped[ColonyHealth] = mapped_column(nullable=False)
    queen_seen: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    honey_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    population_estimate: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    inspected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    hive: Mapped["Hive"] = relationship(back_populates="inspections")
    photos: Mapped[list["InspectionPhoto"]] = relationship(
        back_populates="inspection", cascade="all, delete-orphan"
    )
    ml_prediction: Mapped["MLPrediction | None"] = relationship(
        back_populates="inspection", uselist=False
    )


class InspectionPhoto(Base):
    __tablename__ = "inspection_photos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    inspection_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inspections.id"), nullable=False
    )

    url: Mapped[str] = mapped_column(String, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    inspection: Mapped["Inspection"] = relationship(back_populates="photos")


class MLPrediction(Base):
    __tablename__ = "ml_predictions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    inspection_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inspections.id"), unique=True, nullable=False
    )

    model_name: Mapped[str] = mapped_column(String(100), nullable=False)
    result: Mapped[dict] = mapped_column(JSONB, nullable=False)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)

    processed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    inspection: Mapped["Inspection"] = relationship(back_populates="ml_prediction")
