from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from src.shared.domain.interfaces.llm import LLMInterface
from src.shared.database import LLM
from src.shared.database.session import get_db

class LLMRepository(LLMInterface):
    def __init__(self, db: Session = Depends(get_db)):
        """
        InMemory LLM Repository.

        Args:
            db (Session, optional): _description_. Defaults to Depends(get_db).
        """
        self.db = db

    
    def get(self) -> List[LLM]:
        """
        Fetch a list of LLM objects from the repository.

        Returns:
            List[LLM]: A list of LLM objects retrieved from the repository.
        """

        return self.db.query(LLM).all()

    def get_one(self, name: str) -> LLM | None:
        """
        Fetch an LLM object from the repository.

        Returns:
            LLM: An LLM object retrieved from the repository.
        """
        
        return self.db.query(LLM).filter(LLM.name == name).first()
