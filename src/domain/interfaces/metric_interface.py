from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Metric

class MetricInterface(ABC):
    """
    Abstract base class for Metric Repository.

    This repository defines the interface for retrieving Metrics.

    Methods:
        get() -> List[Metric]:
            Retrieve a list of LLM objects from the repository.

        get_one(title: str) -> Metric:
            Retrieve a details of an llm by title.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type[Exception], exc_value: str, exc_traceback: str):
        pass

    @abstractmethod
    def get(self) -> List[Metric]:
        """
        Fetch a list of Metric objects from the repository.

        Returns:
            List[Metric]: A list of Metric objects retrieved from the repository.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def get_one(self, title: str) -> Metric | None:
        """
        Fetch a Metric object from the repository.

        Returns:
            Metric: A Metric object retrieved from the repository.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()
