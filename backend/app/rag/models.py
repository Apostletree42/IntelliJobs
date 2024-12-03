from beanie import Document
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from ..auth.models import PyObjectId

class QueryRequest(BaseModel):
   query: str

class QueryResponse(BaseModel):
   text: str
   sender: str = "bot"
   contexts: Optional[List[str]] = None
   user: Optional[str] = None

class Conversation(Document):
   id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
   user_id: str
   messages: List[dict] = []
   created_at: datetime = Field(default_factory=datetime.utcnow)
   updated_at: datetime = Field(default_factory=datetime.utcnow)

   class Settings:
       name = "conversations"
       
   class Config:
       json_encoders = {PyObjectId: str}
       populate_by_name = True
       arbitrary_types_allowed = True

