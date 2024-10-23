from sqlalchemy import Column, String
from src.infrastructure.database.base import Base

class Metric(Base):
    __tablename__ = "metrics"
    title = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<Metric(id={self.id}, title={self.title}>"
