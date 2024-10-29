from sqlalchemy import Column, Float, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.shared.database.models.base import Base


class Benchmark(Base):
    __tablename__ = "benchmarks"
    value = Column(Float, nullable=False)
    llm_id = Column(UUID(as_uuid=True), ForeignKey("llms.id"), nullable=False)
    metric_id = Column(UUID(as_uuid=True), ForeignKey("metrics.id"), nullable=False)
    llm = relationship("LLM")
    metric = relationship("Metric")

    __table_args__ = (
        Index("benchmarks_llm_id_idx", llm_id),
        Index("benchmarks_metric_id_idx", metric_id),
    )

    def __repr__(self):
        return (
            f"<Benchmark(id={self.id}, value={self.value}, llm_id={self.llm_id}, "
            f"metric_id={self.metric_id}, llm={self.llm}, metric={self.metric}>"
        )
