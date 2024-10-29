from sqlalchemy.orm import Session

from src.randomiser_service.database.seeders import populate_llms, populate_metrics


async def seed_data(db: Session):
    await populate_llms(db)
    await populate_metrics(db)
