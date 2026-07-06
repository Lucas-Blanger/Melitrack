from pydantic import BaseModel

from .inspection import InspectionResponse


class DashboardOverview(BaseModel):
    total_hives: int
    last_inspection: InspectionResponse | None = None
    health_alerts: int
