from functools import lru_cache
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationSummaryBufferMemory
from typing import List, Dict, Any
from ..config import Settings

@lru_cache()
def get_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert at answering questions based on provided context.
        Please provide accurate, relevant responses using the following context: {context}
        Consider the conversation history for better context: {history}
        If the context doesn't contain enough information to answer the question fully,
        acknowledge this and provide the best possible answer based on available information."""),
        ("human", "{question}"),
    ])

@lru_cache()
def get_llm(api_key: str, model_name: str, temperature: float) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model=model_name,
        temperature=temperature
    )

def generate_response(
    query: str, 
    contexts: List[Dict[str, Any]], 
    memory: ConversationSummaryBufferMemory,
    settings: Settings
) -> str:
    llm = get_llm(
        settings.GOOGLE_API_KEY,
        settings.LLM_MODEL_NAME,
        settings.LLM_TEMPERATURE
    )
    prompt = get_prompt_template()
    
    combined_context = '\n\n'.join(match['metadata']['text'] for match in contexts)
    history = memory.load_memory_variables({})
    
    chain = prompt | llm
    response = chain.invoke({
        "context": combined_context,
        "history": history,
        "question": query
    })
    
    return response.content