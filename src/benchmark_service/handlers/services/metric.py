from fastapi import Depends

from src.benchmark_service.handlers.use_cases.metric import MetricUseCases
from src.shared.domain.repositories.metric import MetricRepository


class MetricService(MetricUseCases):
    def __init__(self, repository: MetricRepository = Depends(MetricRepository)):
        super().__init__(repository)

    def get_metrics(self):
        """
        Retrieves all metrics
        """

        metrics = self.repository.get()
        return {"status": "success", "data": metrics}

    def store_metric(self, title: str, upper_bound: float, lower_bound: float) -> dict:
        """
        Stores a metric
        """

        res = self.repository.store(title, upper_bound, lower_bound)
        return {"status": "success", "data": res}
