from enum import Enum

from fastapi import status
from fastapi.routing import APIRouter

from src.benchmark_service.api.routers import benchmark, llm, metric
from src.benchmark_service.config import config

router = APIRouter()


class StatusEnum(str, Enum):
    OK = "success"
    FAILURE = "failed"
    ERROR = "error"
    UNKNOWN = "unknown"


@router.get(
    "/status",
    status_code=status.HTTP_200_OK,
    tags=["Health Check"],
    summary="Performs health check",
    description="Performs health check and returns information about running service.",
)
def health_check():
    return {
        "status": StatusEnum.OK,
        "data": {
            "title": config.APP_NAME,
            "version": config.APP_VERSION,
        },
    }


router.include_router(
    benchmark.router, prefix="/api/v1/benchmarks", tags=["Benchmark Rankings"]
)
router.include_router(metric.router, prefix="/api/v1/metrics", tags=["Metrics"])
router.include_router(
    llm.router, prefix="/api/v1/llms", tags=["Language Learning Models"]
)
