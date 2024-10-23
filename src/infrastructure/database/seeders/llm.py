from sqlalchemy.orm import Session
from database import LLM
from utils.logger import logging

def seed_llms(db: Session):
    if db.query(LLM).count() > 0:
        logging.info("Seeding skipped. Records exist")
        return

    llms = [
        {"name": "GPT-4o", "creator": "OpenAI"},
        {"name": "Llama 3.1 405", "creator": "Meta"},
        {"name": "Claude 3.5 Sonnet", "creator": "Anthropic"},
    ]

    for llm in llms:
        record = LLM(name=llm["name"], creator=llm["creator"])
        db.add(record)

    db.commit()
    logging.info("LLMs seeded successfully.")
