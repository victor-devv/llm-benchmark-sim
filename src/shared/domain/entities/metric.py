from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


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


class MetricSingleResponse(BaseModel):
    status: str
    data: MetricEntity
