from sqlalchemy.orm import Session

from src.shared.database.models.metric import Metric
from src.shared.utils.logger import logging


async def populate_metrics(db: Session) -> None:
    if db.query(Metric).count() > 0:
        logging.info("Seeding: Populate Metrics skipped. Metrics exist")
        return

    metrics = [
        "ttft",
        "tps",
        "e2e_latency",
        "rps",
    ]

    ranges = {
        "ttft": (0.05, 2.0),  # Time to First Token (seconds)
        "tps": (10.0, 150.0),  # Tokens Per Second
        "e2e_latency": (0.2, 10.0),  # End-to-End Request Latency (seconds)
        "rps": (1.0, 100.0),  # Requests Per Second
    }

    for metric in metrics:
        record = Metric(
            title=metric, lower_bound=ranges[metric][0], upper_bound=ranges[metric][1]
        )
        db.add(record)

    db.commit()
    logging.info("Metrics seeded successfully.")
