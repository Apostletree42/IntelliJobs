from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict, Any
from ..config import Settings

def get_prompt_template() -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", """You are an expert at answering questions based on provided context. 
        Please provide accurate, relevant responses using the following context: {context}
        If the context doesn't contain enough information to answer the question fully, 
        acknowledge this and provide the best possible answer based on available information."""),
        ("human", "{question}"),
    ])

def get_llm(settings: Settings) -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        google_api_key=settings.GOOGLE_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=settings.LLM_TEMPERATURE
    )

def generate_response(query: str, contexts: List[Dict[str, Any]], settings: Settings) -> str:
    # Initialize components
    llm = get_llm(settings)
    prompt = get_prompt_template()
    
    # Prepare context
    combined_context = '\n\n'.join(match['metadata']['text'] for match in contexts)
    
    # Generate response
    chain = prompt | llm
    response = chain.invoke({
        "context": combined_context,
        "question": query
    })
    
    return response.content