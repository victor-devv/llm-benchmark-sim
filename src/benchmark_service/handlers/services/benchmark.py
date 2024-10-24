import json
from src.shared.domain.repositories.benchmark import BenchmarkRepository
from src.shared.domain.repositories.llm import LLMRepository
from src.shared.domain.repositories.metric import MetricRepository
from src.shared.redis.redis import RedisClient, RedisKeys
from src.benchmark_service.handlers.use_cases.benchmark import BenchmarkUseCases
from fastapi import Depends, HTTPException


class BenchmarkService(BenchmarkUseCases):
    def __init__(self, benchmark_repository: BenchmarkRepository = Depends(BenchmarkRepository), llm_repository: LLMRepository = Depends(LLMRepository), metric_repository: MetricRepository = Depends(MetricRepository)):
        super().__init__(benchmark_repository, llm_repository, metric_repository)

    def rank_simulations(self):
        """
        Retrieves all metrics and their corresponding simulations, then ranks the llms based on their means.
        """

        redis_client = RedisClient()
        if redis_client.redis.exists(RedisKeys.BENCHMARKS.value):
            redis_results = json.loads(redis_client.redis.get(RedisKeys.BENCHMARKS.value))
            return {"status": "success", "data": redis_results}

        metrics = self.metric_repository.get()
        results = []

        for metric in metrics:
            benchmarks = self.benchmark_repository.get_one(metric.title)

            if len(benchmarks) > 0:
                result = [
                    {"llm": benchmark[0], "mean": round(benchmark[1], 2)}
                    for benchmark in benchmarks
                ]

                results.append(({metric.title: result}))

        if len(results) > 0:
            redis_client.redis.set(RedisKeys.BENCHMARKS.value, json.dumps(results))

        return {"status": "success", "data": results}

    def rank_simulation_by_metric(self, metric_title):
        """
        Retrieves a metric and its corresponding simulations, then ranks the llms based on the mean values.
        """
        redis_client = RedisClient()
        if redis_client.redis.exists(f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric_title}"):
            redis_results = json.loads(redis_client.redis.get(f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric_title}"))
            return {"status": "success", "data": redis_results}

        metric = self.metric_repository.get_one(metric_title)
        if not metric:
            raise HTTPException(status_code=404, detail="Metric not found")

        benchmarks = self.benchmark_repository.get_one(metric.title)

        if len(benchmarks) > 0:
            result = [
                {"llm": benchmark[0], "mean": round(benchmark[1], 2)} for benchmark in benchmarks
            ]

            redis_client.redis.set(f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric_title}", json.dumps(result))
        else:
            result = []

        return {"status": "success", "data": result}
           