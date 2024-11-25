from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    text: str
    sender: str = "bot"
    contexts: Optional[List[str]] = None
    user: Optional[str] = None