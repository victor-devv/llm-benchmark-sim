from fastapi import APIRouter, Depends, HTTPException, status

from src.benchmark_service.api.routers.auth import validate_api_key
from src.benchmark_service.handlers.services.metric import MetricService
from src.shared.domain.entities.metric import (
    CreateMetricDto,
    MetricResponse,
    MetricSingleResponse,
)

router = APIRouter()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=MetricResponse,
    description="Returns all available quality metrics",
)
def get_all_metrics(
    metric_service: MetricService = Depends(MetricService),
    api_key: str = Depends(validate_api_key),
):
    response = metric_service.get_metrics()
    return response


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=MetricSingleResponse,
    description="Creates a quality metric using the upper and lower range values",
)
def create(
    metric: CreateMetricDto,
    metric_service: MetricService = Depends(MetricService),
    api_key: str = Depends(validate_api_key),
):
    try:
        response = metric_service.store_metric(
            title=metric.title,
            upper_bound=metric.upper_bound,
            lower_bound=metric.lower_bound,
        )
        return response
    except Exception:
        raise HTTPException(status_code=400, detail="error creating metric")
