from pydantic import BaseModel

class RAGQuery(BaseModel):
    query: str

class RAGResponse(BaseModel):
    response: str