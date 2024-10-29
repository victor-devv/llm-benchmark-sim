from fastapi import Depends

from src.benchmark_service.handlers.use_cases.llm import LLMUseCases
from src.shared.domain.repositories.llm import LLMRepository


class LLMService(LLMUseCases):
    def __init__(self, repository: LLMRepository = Depends(LLMRepository)):
        super().__init__(repository)

    def get_llms(self):
        """
        Retrieves all llms
        """

        res = self.repository.get()
        return {"status": "success", "data": res}

    def store_llm(self, name: str, creator: str):
        """
        Stores an llm
        """

        res = self.repository.store(name, creator)
        return {"status": "success", "data": res}
