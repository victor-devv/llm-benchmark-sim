from typing import List, Optional
from uuid import UUID
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, insert
from src.domain.interfaces import BenchmarkRepositoryInterface
from src.domain.entities import Benchmark, LLM, Metric
from src.infrastructure.database.session import get_db

class BenchmarkRepository(BenchmarkRepositoryInterface):
    def __init__(self, db: Session = Depends(get_db)):
        """
        InMemory BenchmarkRepository.

        Args:
            db (Session, optional): _description_. Defaults to Depends(get_db).
        """
        self.db = db

    
    def get(self) -> List[Benchmark]:
        """
        Fetch a list of Benchmark objects from the repository.

        Returns:
            List[Metric]: A list of Benchmark objects retrieved from the repository.
        """

        return self.db.query(Benchmark).all()

    def get_one(self, metric_title: str) -> Optional[List[tuple]]:
        """
        Fetch Benchmark results for a given metric.

        Args:
            metric_title (str): The title of the metric

        Returns:
            Optional[List[tuple]]: A list of tuples containing the LLM name and mean metric value,
            or None if no results found.
        """
        
        query = (
            self.db.query(
                LLM.name.label("llm_name"),
                func.avg(Benchmark.value).label("mean_value"),
            )
            .join(Benchmark.llm)
            .join(Benchmark.metric)
            .filter(Metric.title == metric_title)
            .group_by(LLM.name, Metric.title)
            .order_by(func.avg(Benchmark.value).desc())
        )

        return query.all() if query.count() > 0 else None

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
        """

        if not benchmarks:
            return 0

        data = [
            {"llm_id": llm_id, "metric_id": metric_id, "value": value}
            for value in benchmarks
        ]

        self.db.execute(insert(Benchmark), data)
        self.db.commit()

        return len(data)

    def delete(self) -> None:
        """
        Deletes all stored benchmarks

        Returns:
            None
        """
        self.db.query(Benchmark).delete(synchronize_session=False)
        self.db.commit()
