from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class LLMEntity(BaseModel):
    id: UUID
    created_at: datetime
    name: str
    creator: str
    updated_at: Optional[datetime]

class CreateLlmDto(BaseModel):
    name: str
    creator: str

class LLMResponse(BaseModel):
    status: str
    data: List[LLMEntity]

class LLMSingleResponse(BaseModel):
    status: str
    data: LLMEntity
