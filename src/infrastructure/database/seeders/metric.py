from sqlalchemy.orm import Session
from database import Metric
from utils.logger import logging

def seed_metrics(db: Session):
    if db.query(Metric).count() > 0:
        logging.info("Seeding skipped. Metrics exist")
        return

    metrics = [
        "ttft",
        "tps",
        "e2e_latency",
        "rps",
    ]

    for metric in metrics:
        record = Metric(title=metric)
        db.add(record)

    db.commit()
    logging.info("Metrics seeded successfully.")
