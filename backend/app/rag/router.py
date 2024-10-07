from fastapi import APIRouter, Depends
from .engine import RAGEngine
from .models import RAGQuery, RAGResponse

router = APIRouter()
rag_engine = RAGEngine()

@router.post("/query", response_model=RAGResponse)
async def rag_query(query: RAGQuery):
    return await rag_engine.process_query(query)