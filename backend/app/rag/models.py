from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from beanie import Document

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    text: str
    sender: str = "bot"
    contexts: Optional[List[str]] = None
    user: Optional[str] = None

class Conversation(Document):
    user_id: str
    messages: List[dict] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "conversations"