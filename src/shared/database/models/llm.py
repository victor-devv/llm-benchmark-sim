from sqlalchemy import Column, String
from src.shared.database.models.base import Base

class LLM(Base):
    __tablename__ = "llms"
    name = Column(String, unique=True, nullable=False)
    creator = Column(String, unique=False, nullable=False)

    def __repr__(self):
        return (
            f"<LLM(id={self.id}, name={self.name}, creator={self.creator})>"
        )
