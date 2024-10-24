from pydantic import BaseModel

class LLMEntity(BaseModel):
    id: str
    name: str
    creator: str
    created_at: str
    updated_at: str

class CreateLlmDto(BaseModel):
    name: str
    creator: str
