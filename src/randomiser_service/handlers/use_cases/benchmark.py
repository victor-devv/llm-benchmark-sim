from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.benchmark import BenchmarkEntity
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
    def delete_all(self) -> List[BenchmarkEntity]:
        raise NotImplemented
    
    @abstractmethod
    def simulate(self) -> List[BenchmarkEntity]:
        raise NotImplemented
