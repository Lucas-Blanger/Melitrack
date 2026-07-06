from datetime import datetime

from pydantic import BaseModel

from apps.hives.models import AnalysisStatus


class AnalysisResponse(BaseModel):
    status: AnalysisStatus
    model_name: str | None = None
    result: dict | None = None
    confidence: float | None = None
    error_message: str | None = None
    processed_at: datetime | None = None
