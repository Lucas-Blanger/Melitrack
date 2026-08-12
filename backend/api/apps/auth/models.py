import uuid
from datetime import datetime

from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from db.base import Base
from db.mixins import TimestampMixin


class User(Base, TimestampMixin):

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    reset_code = Column(String, nullable=True)
    reset_code_expires = Column(DateTime(timezone=True), nullable=True)
    google_id = Column(String, unique=True, nullable=True)
    picture = Column(String, nullable=True)
    auth_provider = Column(String, nullable=False, default="local")

    # Settings & Preferences
    meliponary_name = Column(String, default="Meu Meliponário", server_default="Meu Meliponário", nullable=True)
    meliponary_location = Column(String, nullable=True)
    inspection_frequency_days = Column(Integer, default=14, server_default="14", nullable=True)
    notify_health_alerts = Column(Boolean, default=True, server_default="true", nullable=True)
    notify_email = Column(Boolean, default=True, server_default="true", nullable=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, name={self.name})>"
