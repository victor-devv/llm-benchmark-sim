from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class MetricEntity(BaseModel):
    id: UUID
    created_at: datetime
    title: str
    upper_bound: float
    lower_bound: float
    updated_at: Optional[datetime]
        
class CreateMetricDto(BaseModel):
    title: str
    upper_bound: float
    lower_bound: float

class MetricResponse(BaseModel):
    status: str
    data: List[MetricEntity]