from abc import ABC, abstractmethod

from src.shared.domain.interfaces.metric import MetricInterface as MetricRepository


class MetricUseCases(ABC):

    @abstractmethod
    def __init__(self, repository: MetricRepository):
        self.repository = repository

    @abstractmethod
    def get_metrics(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def store_metric(self, title: str, upper_bound: float, lower_bound: float) -> dict:
        raise NotImplementedError
