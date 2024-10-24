from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from src.shared.domain.entities.benchmark import BenchmarkEntity

class BenchmarkInterface(ABC):
    """
    Abstract base class for Benchmark Repository.

    This repository defines the interface for retrieving LLM Metric Benchmarks.

    Methods:
        get() -> List[BenchmarkBenchmark]:
            Retrieve all stored benchmarks from the repository.

        get_one(metric_name: str) -> Benchmark:
            Retrieve a details of an llm by name.

        store(metric_id: UUID, benchmarks: List[Benchmark]) -> None:
            Saves benchmarks to the repository.

        delete() -> Benchmark:
            Deletes all stored benchmarks.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type[Exception], exc_value: str, exc_traceback: str):
        pass

    @abstractmethod
    def get(self) -> List[BenchmarkEntity]:
        """
        Fetch a list of Benchmark objects from the repository.

        Returns:
            List[Benchmark]: A list of Benchmark objects retrieved from the repository.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def get_one(self, metric_name: str) -> Optional[List[tuple]]:
        """
        Retrieves the mean simulation benchmark values for a given metric.

        Args:
            metric_name (str): The name of the metric to filter by. If not provided, all metrics are considered.

        Returns:
            Optional[List[tuple]]: A list of tuples containing the LLM name and mean metric value,
            or None if no results found.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def store(
        self, llm_id: UUID, metric_id: UUID, benchmarks: List[float]
    ) -> int:
        """
        Stores benchmarks to the database.

        Args:
            llm_id (UUID): The ID of the LLM.
            metric_id (UUID): The ID of the metric.
            benchmarks (List[float]): list of benchmark values to be added.

        Returns:
            int: The number of benchmarks added.
        
        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self) -> None:
        """
        Deletes all stored benchmarks

        Returns:
            None

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()
