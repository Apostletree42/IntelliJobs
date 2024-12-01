from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .models import QueryRequest, QueryResponse
from .engine import process_query
from ..config import get_settings, Settings
from ..auth.dependencies import get_current_user
from ..auth.models import User

rag_router = APIRouter(prefix="/rag", tags=["rag"])

@rag_router.post("/query", response_model=QueryResponse)
async def handle_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings)
) -> QueryResponse:
    
    response = process_query(request.query, settings)
    response.user = current_user.username 
    return response

# Optional: Add an endpoint to get user's query history
@rag_router.get("/history", response_model=List[QueryResponse])
async def get_query_history(
    current_user: User = Depends(get_current_user),
    settings: Settings = Depends(get_settings)
) -> List[QueryResponse]:
    # Here you would typically fetch the user's query history from your database
    # For example:
    # history = await get_user_query_history(current_user.username)
    # return history
    
    # Placeholder response
    return []