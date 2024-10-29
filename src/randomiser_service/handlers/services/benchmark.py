import os
import traceback
from typing import List

import redis
from dotenv import load_dotenv

from src.randomiser_service.handlers.use_cases.benchmark import BenchmarkUseCases
from src.randomiser_service.utils.randomizer import generate_data_points
from src.randomiser_service.utils.retry import retry
from src.shared.domain.entities.benchmark import BenchmarkEntity
from src.shared.domain.entities.llm import LLMEntity
from src.shared.domain.entities.metric import MetricEntity
from src.shared.domain.repositories.benchmark import BenchmarkRepository
from src.shared.domain.repositories.llm import LLMRepository
from src.shared.domain.repositories.metric import MetricRepository
from src.shared.redis.redis import RedisClient, RedisKeys
from src.shared.utils.logger import logging

load_dotenv()

MAX_RETRIES = int(os.getenv("MAX_RETRIES", "2"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "60"))


class BenchmarkService(BenchmarkUseCases):

    def __init__(
        self,
        benchmark_repository: BenchmarkRepository,
        llm_repository: LLMRepository,
        metric_repository: MetricRepository,
    ):
        super().__init__(benchmark_repository, llm_repository, metric_repository)

    def delete_all(self):
        self.benchmark_repository.delete()

    @retry(redis_client=RedisClient(), max_retries=MAX_RETRIES, delay=RETRY_DELAY)
    async def generate_benchmark_data(
        self, lower_bound: float, upper_bound: float, metric: str, llm: str
    ):
        return generate_data_points(lower_bound, upper_bound, metric, llm)

    async def simulate(self) -> List[BenchmarkEntity]:
        llms: List[LLMEntity] = self.llm_repository.get()
        metrics: List[MetricEntity] = self.metric_repository.get()

        self.delete_all()

        redis_client = RedisClient()

        for llm in llms:
            for metric in metrics:
                metric_values = await self.generate_benchmark_data(
                    metric.lower_bound, metric.upper_bound, metric.title, llm.name
                )

                if metric_values:
                    self.benchmark_repository.store(llm.id, metric.id, metric_values)

                    redis_client.redis.delete(
                        f"{RedisKeys.RETRY_BENCHMARKS.value}:{llm.id}:{metric.id}"
                    )

                    if redis_client.redis.exists(
                        f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric.title}"
                    ):
                        redis_client.delete_key(
                            f"{RedisKeys.METRIC_BENCHMARKS.value}:{metric.title}"
                        )

        logging.info("Benchmark simulation completed successfully")

        if redis_client.redis.exists(RedisKeys.BENCHMARKS.value):
            redis_client.delete_key(RedisKeys.BENCHMARKS.value)

    async def initiate_simulation(self):
        redis_client = RedisClient()

        try:
            with redis_client.redis.lock(
                RedisKeys.RETRY_BENCHMARKS_LOCK.value,
                timeout=MAX_RETRIES * RETRY_DELAY,
                blocking=True,
                blocking_timeout=10,
            ) as lock:
                await self.simulate()
        except redis.exceptions.LockError as lockError:
            logging.error(f"Redis lock error: {lockError}")
        except Exception as e:
            traceback.print_exc()
            logging.error(f"Error simulating data points: {e}")
        finally:
            if "lock" in locals() and lock.locked():
                try:
                    lock.release()
                except redis.exceptions.LockError:
                    logging.info("Lock already released")
