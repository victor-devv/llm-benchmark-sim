from abc import ABC, abstractmethod

from src.shared.domain.interfaces.llm import LLMInterface as LLMRepository


class LLMUseCases(ABC):

    @abstractmethod
    def __init__(self, repository: LLMRepository):
        self.repository = repository

    @abstractmethod
    def get_llms(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def store_llm(self, name: str, creator: str) -> dict:
        raise NotImplementedError
