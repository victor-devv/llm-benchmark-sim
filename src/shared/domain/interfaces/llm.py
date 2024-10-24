from abc import ABC, abstractmethod
from typing import List
from src.shared.domain import LLM

class LLMInterface(ABC):
    """
    Abstract base class for LLM Repository.

    This repository defines the interface for storing and retrieving LLMs.
    Implementations of this repository should handle the persistence details, whether
    it's a database, in-memory storage, or any other data storage solution.

    Methods:
        store(results: LLM) -> None:
            Save an LLM object to the repository.

        get() -> List[LLM]:
            Retrieve a list of LLM objects from the repository.

        get_one(name: str) -> LLM:
            Retrieve a details of an llm by name.
    """

    def __enter__(self):
        return self

    def __exit__(self, exc_type: type[Exception], exc_value: str, exc_traceback: str):
        pass

    @abstractmethod
    def get(self) -> List[LLM]:
        """
        Fetch a list of LLM objects from the repository.

        Returns:
            List[LLM]: A list of LLM objects retrieved from the repository.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_one(self, name: str) -> LLM | None:
        """
        Fetch an LLM object from the repository.

        Returns:
            LLM: An LLM object retrieved from the repository.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def store(self, name: str, creator: str) -> None:
        """
        Save an LLM object to the repository.

        Args:
            name: str, 
            creator: str

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError()

