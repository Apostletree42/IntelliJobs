from datetime import datetime
from langchain.memory import ConversationSummaryBufferMemory
from langchain_google_genai import ChatGoogleGenerativeAI
from .generator import generate_response, get_llm
from .retriever import get_relevant_contexts
from ..config import Settings
from .models import Conversation, QueryResponse
import google.generativeai as genai

class RAGEngine:
    def __init__(self, settings: Settings, user_id: str):
        self.settings = settings
        self.user_id = user_id
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=self.settings.GOOGLE_API_KEY
        )
        self.conversation_history = []

    async def process_query(self, query: str) -> QueryResponse:
        try:
            contexts = get_relevant_contexts(query, self.settings)
            context_text = "\n\n".join([match['metadata']['text'] for match in contexts])
            
            self.conversation_history.append({"role": "user", "content": query})
            
            augmented_prompt = f"""You are a conversational job search assistant. Be natural and friendly while providing accurate information.

    Previous messages:
    {self._format_history()}

    Job listings context:
    {context_text}

    Question: {query}

    Provide a natural, conversational response that builds on our previous discussion if relevant."""

            response = self.llm.invoke(augmented_prompt)
            self.conversation_history.append({"role": "assistant", "content": response.content})
            
            return QueryResponse(
                text=response.content,
                contexts=[match['metadata']['text'] for match in contexts],
                user=self.user_id
            )
        except Exception as e:
            print(f"Error in process_query: {str(e)}")
            raise

    def _format_history(self) -> str:
        return "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history[-4:]])  # Keep last 2 turns