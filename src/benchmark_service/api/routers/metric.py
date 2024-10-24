from fastapi import APIRouter, Depends, status
from src.benchmark_service.handlers.services.metric import MetricService
from src.benchmark_service.api.routers.auth import validate_api_key
 
router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def get_metrics(
    metric_service: MetricService = Depends(MetricService),
    api_key: str = Depends(validate_api_key),
):
    response = metric_service.get_metrics()
    return response

