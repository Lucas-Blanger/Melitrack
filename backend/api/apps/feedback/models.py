import uuid

from sqlalchemy import CheckConstraint, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base
from db.mixins import TimestampMixin


class FeedbackResponse(Base, TimestampMixin):
    __tablename__ = "feedback_responses"
    __table_args__ = (
        CheckConstraint(
            "enjoyment IN ('gostando', 'neutro', 'nao_gostando')",
            name="ck_feedback_responses_enjoyment",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    enjoyment: Mapped[str] = mapped_column(String(20), nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=False)
    suggestions: Mapped[str | None] = mapped_column(Text, nullable=True)
