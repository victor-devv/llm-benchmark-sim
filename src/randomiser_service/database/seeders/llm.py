from sqlalchemy.orm import Session
from src.shared.database.models.llm import LLM
from src.shared.utils.logger import logging

async def populate_llms(db: Session) -> None:
    if db.query(LLM).count() > 0:
        logging.info("Seeding: Populate LLM skipped. Records exist")
        return

    llms = [
        {"name": "GPT-4o", "creator": "OpenAI"},
        {"name": "Llama 3.1 405", "creator": "Meta"},
        {"name": "Claude 3.5 Sonnet", "creator": "Anthropic"},
        {"name": "Gemini 1.5Flash", "creator": "Google"},
    ]

    for llm in llms:
        record = LLM(name=llm["name"], creator=llm["creator"])
        db.add(record)

    db.commit()
    logging.info("LLMs seeded successfully.")
