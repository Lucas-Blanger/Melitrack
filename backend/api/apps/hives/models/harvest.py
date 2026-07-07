import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.mixins import TimestampMixin

if TYPE_CHECKING:
    from apps.hives.models.product import Product
    from apps.hives.models.enums import Hive


class Harvest(Base, TimestampMixin):
    __tablename__ = "harvests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    hive_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("hives.id"), nullable=False, index=True
    )
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)

    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    quality_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    harvested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )

    hive: Mapped["Hive"] = relationship(back_populates="harvests")
    product: Mapped["Product"] = relationship(back_populates="harvests")
