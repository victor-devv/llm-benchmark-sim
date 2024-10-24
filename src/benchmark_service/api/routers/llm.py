from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from src.benchmark_service.handlers.services.llm import LLMService
from src.benchmark_service.api.routers.auth import validate_api_key
from src.shared.domain.entities.llm import LLMResponse, LLMSingleResponse, CreateLlmDto

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK, response_model=LLMResponse, description="Returns all available language learning models.")
def get_all_language_learning_models(
    llm_service: LLMService = Depends(LLMService),
    api_key: str = Depends(validate_api_key),
):
    response = llm_service.get_llms()
    return response

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=LLMSingleResponse, description="Creates language learning models.")
def create(llm: CreateLlmDto, llm_service: LLMService = Depends(LLMService), api_key: str = Depends(validate_api_key),):
    try:
        response = llm_service.store_llm(
            name=llm.name,
            creator=llm.creator
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail="error creating LLM")
    