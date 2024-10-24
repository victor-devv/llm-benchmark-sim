from abc import ABC, abstractmethod
from src.shared.domain.interfaces.metric import MetricInterface as MetricRepository


class MetricUseCases(ABC):

    @abstractmethod
    def __init__(self, repository: MetricRepository):
        self.repository = repository

    @abstractmethod
    def get_metrics(self) -> dict:
        raise NotImplemented
    
