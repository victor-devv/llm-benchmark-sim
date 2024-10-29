from sqlalchemy import Column, Numeric, String

from src.shared.database.models.base import Base


class Metric(Base):
    __tablename__ = "metrics"
    title = Column(String, unique=True, nullable=False)
    upper_bound = Column(Numeric, unique=True, nullable=False)
    lower_bound = Column(Numeric, unique=True, nullable=False)

    def __repr__(self):
        return (
            f"<Metric(id={self.id}, title={self.title}, "
            f"upper_bound={self.upper_bound}, lower_bound={self.lower_bound})>"
        )
