import pytest
from unittest.mock import AsyncMock, Mock, patch
from src.randomiser_service.handlers.services.benchmark import MAX_RETRIES, RETRY_DELAY, BenchmarkService


@pytest.fixture
def mock_llm_repository():
    return Mock()


@pytest.fixture
def mock_metric_repository():
    return Mock()


@pytest.fixture
def mock_benchmark_repository():
    return Mock()


@pytest.fixture
def benchmark_service(mock_llm_repository, mock_metric_repository, mock_benchmark_repository):
    return BenchmarkService(
        llm_repository=mock_llm_repository,
        metric_repository=mock_metric_repository,
        benchmark_repository=mock_benchmark_repository,
    )

@pytest.fixture
def mock_redis_client():
    with patch("src.randomiser_service.handlers.services.benchmark.RedisClient") as mock:
        yield mock.return_value


@pytest.mark.asyncio
async def test_generate_benchmark_data(benchmark_service):
    mock_metric_generator = Mock()
    mock_metric_generator.generate_data_points.return_value = [1, 2, 3]
    metric_title = "test_metric"
    llm_name = "test_engine"

    result = await benchmark_service.generate_benchmark_data(
        mock_metric_generator, metric_title, llm_name
    )

    assert result == [1, 2, 3]
    mock_metric_generator.generate_data_points.assert_called_once_with(metric_title)


@pytest.mark.asyncio
async def test_initiate_simulation_success(
    benchmark_service, mock_redis_client
):
    mock_lock = AsyncMock()
    mock_redis_client.redis.lock.return_value.__enter__.return_value = mock_lock

    with patch.object(
        benchmark_service, "simulate", new_callable=AsyncMock
    ) as mock_simulate:
        await benchmark_service.initiate_simulation()
        mock_redis_client.redis.lock.assert_called_once_with(
            "retry_benchmarks_lock",
            timeout=MAX_RETRIES * RETRY_DELAY,
            blocking=True,
            blocking_timeout=10,
        )
        mock_simulate.assert_called_once()


@pytest.mark.asyncio
async def test_simulate(
    benchmark_service,
    mock_llm_repository,
    mock_metric_repository,
    mock_benchmark_repository,
    mock_redis_client,
):
    mock_llm = Mock()
    mock_llm.id = 1
    mock_llm.name = "TestLLM"
    mock_llm.creator = "TestCompany"
    mock_llm_repository.get_llms.return_value = [mock_llm]

    mock_metric = Mock()
    mock_metric.id = 1
    mock_metric.title = "TestMetric"
    mock_metric_repository.get_metrics.return_value = [mock_metric]

    with patch(
        "src.randomiser_service.handlers.services.benchmark.MetricGenerator"
    ) as mock_generator_class:
        mock_generator = Mock()
        mock_generator_class.return_value = mock_generator
        mock_generator.generate_data_points.return_value = [1, 2, 3]

        await benchmark_service.simulate_data_points()

        mock_benchmark_repository.remove_all_metrics.assert_called_once()
        mock_generator_class.assert_called_once_with("TestCompany", "TestLLM")
        mock_generator.generate_data_points.assert_called_once_with("TestMetric")
        mock_benchmark_repository.bulk_add_metrics.assert_called_once_with(
            1, 1, [1, 2, 3]
        )
        mock_redis_client.redis.delete.assert_called()
        mock_redis_client.delete_key.assert_called()


def test_remove_metrics(benchmark_service, mock_benchmark_repository):
    benchmark_service.delete_all()
    mock_benchmark_repository.remove_all_metrics.assert_called_once()
