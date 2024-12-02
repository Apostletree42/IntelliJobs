from datetime import datetime
from langchain.memory import ConversationSummaryBufferMemory
from .generator import generate_response, get_llm
from .retriever import get_relevant_contexts
from ..config import Settings
from .models import Conversation, QueryResponse

class RAGEngine:
    def __init__(self, settings: Settings, user_id: str):
        self.settings = settings
        self.user_id = user_id
        self.memory = ConversationSummaryBufferMemory(
            llm=get_llm(settings),
            max_token_limit=2000,
            return_messages=True
        )

    async def process_query(self, query: str) -> QueryResponse:
        contexts = get_relevant_contexts(query, self.settings)
        self.memory.save_context({"input": query}, {})
        
        response_text = generate_response(
            query=query,
            contexts=contexts,
            memory=self.memory,
            settings=self.settings
        )

        await self._save_to_mongo(query, response_text)
        return QueryResponse(text=response_text, contexts=[c['metadata']['text'] for c in contexts])

    async def _save_to_mongo(self, query: str, response: str):
        conversation = await Conversation.find_one({"user_id": self.user_id}) or \
                      Conversation(user_id=self.user_id)
        
        conversation.messages.append({
            "role": "user",
            "content": query,
            "timestamp": datetime.now()
        })
        conversation.messages.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now()
        })
        conversation.updated_at = datetime.now()
        await conversation.save()