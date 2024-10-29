from fastapi import APIRouter, Depends, status

from src.benchmark_service.api.routers.auth import validate_api_key
from src.benchmark_service.handlers.services.benchmark import BenchmarkService
from src.shared.domain.entities.benchmark import (
    BenchmarkRankingResponse,
    MetricBenchmarkRankingResponse,
)

router = APIRouter()


@router.get(
    "/rankings",
    status_code=status.HTTP_200_OK,
    response_model=BenchmarkRankingResponse,
    description="Returns LLM rankings for every quality metric.",
)
def get_all_benchmark_rankings(
    benchmark_service: BenchmarkService = Depends(BenchmarkService),
    api_key: str = Depends(validate_api_key),
):
    response = benchmark_service.rank_simulations()
    return response


@router.get(
    "/rankings/{metric}",
    status_code=status.HTTP_200_OK,
    response_model=MetricBenchmarkRankingResponse,
    description="Returns LLM rankings for a specific quality metric.",
)
def get_benchmark_rankings_by_metric_name(
    metric: str,
    benchmark_service: BenchmarkService = Depends(BenchmarkService),
    api_key: str = Depends(validate_api_key),
):
    response = benchmark_service.rank_simulation_by_metric(metric)
    return response
