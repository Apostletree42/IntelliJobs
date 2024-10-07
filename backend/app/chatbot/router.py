from fastapi import APIRouter, Depends
from .service import ChatbotService
from .models import ChatMessage, ChatResponse

router = APIRouter()
chatbot_service = ChatbotService()

@router.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    return await chatbot_service.process_message(message)