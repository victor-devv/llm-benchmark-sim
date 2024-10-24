from pydantic import BaseModel

class BenchmarkEntity(BaseModel):
    id: str
    llm_id: str
    metric_id: str
    value: float
    created_at: str
    updated_at: str

class CreateBenchmarkDto(BaseModel):
    llm_id: str
    metric_id: str
    value: float
