from pydantic import BaseModel

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
        