from typing import List
from fastapi import APIRouter, Depends, status
from src.benchmark_service.handlers.services.llm import LLMService
from src.benchmark_service.api.routers.auth import validate_api_key
from src.shared.domain.entities.llm import LLMEntity

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[LLMEntity],
    description="Returns all available language learning models.")
def get_all_language_learning_models(
    llm_service: LLMService = Depends(LLMService),
    api_key: str = Depends(validate_api_key),
):
    response = llm_service.get_llms()
    return response

