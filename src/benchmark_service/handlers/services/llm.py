from src.shared.domain.repositories.llm import LLMRepository
from src.benchmark_service.handlers.use_cases.llm import LLMUseCases
from fastapi import Depends


class LLMService(LLMUseCases):
    def __init__(self, repository: LLMRepository = Depends(LLMRepository)):
        super().__init__(repository)

    def get_llms(self):
        """
        Retrieves all llms 
        """

        res = self.repository.get()
        return {"status": "success", "data": res}

           