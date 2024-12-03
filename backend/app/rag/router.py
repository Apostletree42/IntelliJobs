import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .models import QueryRequest, QueryResponse, Conversation
from .engine import RAGEngine
from ..config import get_settings, Settings
from ..auth.dependencies import get_current_user
from ..auth.models import User

rag_router = APIRouter(prefix="/rag", tags=["rag"])

# router.py
@rag_router.post("/query", response_model=QueryResponse)
async def handle_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings)
) -> QueryResponse:
    
    engine = RAGEngine(settings, current_user.username)
    return await engine.process_query(request.query)

@rag_router.get("/history", response_model=List[dict])
async def get_query_history(
    current_user: User = Depends(get_current_user)
) -> List[dict]:
    conversation = await Conversation.find_one({"user_id": current_user.username})
    return conversation.messages if conversation else []