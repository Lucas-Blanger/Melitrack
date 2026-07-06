from datetime import datetime

from pydantic import BaseModel


class PhotoResponse(BaseModel):
    id: str
    filename: str
    content_type: str
    size: int
    uploaded_at: datetime
