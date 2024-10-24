from pydantic import BaseModel
from typing import List

class MetricEntity(BaseModel):
    id: str
    title: str
    upper_bound: float
    lower_bound: float
    created_at: str
    updated_at: str
        
class CreateMetricDto(BaseModel):
    title: str
    upper_bound: float
    lower_bound: float

class MetricResponse(BaseModel):
    status: str
    data: List[MetricEntity]