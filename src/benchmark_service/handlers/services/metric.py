from src.shared.domain.repositories.metric import MetricRepository
from src.benchmark_service.handlers.use_cases.metric import MetricUseCases
from fastapi import Depends


class MetricService(MetricUseCases):
    def __init__(self, repository: MetricRepository = Depends(MetricRepository)):
        super().__init__(repository)

    def get_metrics(self):
        """
        Retrieves all metrics 
        """

        metrics = self.repository.get()
        return {"status": "success", "data": metrics}

           