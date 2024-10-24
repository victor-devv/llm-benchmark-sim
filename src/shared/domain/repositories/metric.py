from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.shared.domain.interfaces.metric import MetricInterface
from src.shared.database import Metric
from src.shared.database.session import get_db

class MetricRepository(MetricInterface):
    def __init__(self, db: Session = Depends(get_db)):
        """
        InMemory MetricRepository.

        Args:
            db (Session, optional): _description_. Defaults to Depends(get_db).
        """
        self.db = db

    
    def get(self) -> List[Metric]:
        """
        Fetch a list of Metric objects from the repository.

        Returns:
            List[Metric]: A list of Metric objects retrieved from the repository.
        """

        return self.db.query(Metric).all()

    def get_one(self, title: str) -> Metric | None:
        """
        Fetch an Metric object from the repository.

        Returns:
            Metric: A Metric object retrieved from the repository.
        """
        
        return self.db.query(Metric).filter(Metric.title == title).first()
