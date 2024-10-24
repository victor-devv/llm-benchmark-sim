from pydantic import BaseModel, RootModel
from typing import List, Dict

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

class BenchmarkRankingResultEntity(BaseModel):
    id: str
    llm_id: str
    metric_id: str
    value: float
    created_at: str
    updated_at: str

class BenchmarkResult(BaseModel):
    llm: str
    mean: float

class MetricData(RootModel):
    root: Dict[str, List[BenchmarkResult]]

class BenchmarkResponse(RootModel):
    root: List[MetricData]