from abc import ABC, abstractmethod
from src.shared.domain.interfaces.benchmark import BenchmarkInterface as BenchmarkRepository
from src.shared.domain.interfaces.llm import LLMInterface as LLMRepository
from src.shared.domain.interfaces.metric import MetricInterface as MetricRepository


class BenchmarkUseCases(ABC):

    @abstractmethod
    def __init__(self, benchmark_repository: BenchmarkRepository, llm_repository: LLMRepository, metric_repository: MetricRepository):
        self.benchmark_repository = benchmark_repository
        self.llm_repository = llm_repository
        self.metric_repository = metric_repository

    @abstractmethod
    def rank_simulations(self) -> dict:
        raise NotImplemented
    
    @abstractmethod
    def rank_simulation_by_metric(self, metric_title: str) -> dict:
        raise NotImplemented
