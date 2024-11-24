from fastapi import APIRouter, Depends
from .models import QueryRequest, QueryResponse
from .engine import process_query
from ..config import get_settings, Settings

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def handle_query(
    request: QueryRequest,
    settings: Settings = Depends(get_settings)
) -> QueryResponse:
    return process_query(request.query, settings)