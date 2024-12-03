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
        
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=2000,
            return_messages=True
        )

    async def process_query(self, query: str) -> QueryResponse:
        try:
            memory_variables = self.memory.load_memory_variables({})
            history = memory_variables.get("history", "")

            contexts = get_relevant_contexts(query, self.settings)
            context_text = "\n\n".join([match['metadata']['text'] for match in contexts])
            
            system_context = """You are a helpful job search assistant. Analyze the job listings and provide friendly, conversational responses.
            When answering questions:
            - Consider the conversation history for context
            - Highlight key insights and patterns
            - Use bullet points for clarity
            - Add brief recommendations or insights when relevant
            - Maintain a helpful, professional tone"""
            
            augmented_prompt = f"""{system_context}

Previous Conversation:
{history}

Job Listings:
{context_text}

User Question: {query}

Please provide a detailed analysis based on these job listings and our conversation history."""

            response = self.llm.invoke(augmented_prompt)
            
            self.memory.save_context(
                {"input": query},
                {"output": response.content}
            )
            
            try:
                await self._save_to_mongo(query, response.content)
            except Exception as e:
                print(f"Error saving to MongoDB: {str(e)}")
                # Continue execution even if MongoDB save fails
            
            return QueryResponse(
                text=response.content,
                contexts=[match['metadata']['text'] for match in contexts],
                user=self.user_id
            )
        except Exception as e:
            print(f"Error in process_query: {str(e)}")
            raise

    async def _save_to_mongo(self, query: str, response: str):
        try:
            conversation = await Conversation.find_one({"user_id": self.user_id}) or \
                          Conversation(user_id=self.user_id)
            
            conversation.messages.append({
                "role": "user",
                "content": query,
                "timestamp": datetime.utcnow()
            })
            conversation.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.utcnow()
            })
            conversation.updated_at = datetime.utcnow()
            await conversation.save()
        except Exception as e:
            print(f"Error saving to MongoDB: {str(e)}")
            raise