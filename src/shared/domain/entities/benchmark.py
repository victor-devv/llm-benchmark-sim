from typing import Dict, List

from pydantic import BaseModel, RootModel


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


class MetricBenchmarkRankingResponse(BaseModel):
    status: str
    data: List[BenchmarkResult]


class MetricDataRoot(RootModel):
    root: Dict[str, List[BenchmarkResult]]


class BenchmarkRankingResponse(BaseModel):
    status: str
    data: List[MetricDataRoot]
