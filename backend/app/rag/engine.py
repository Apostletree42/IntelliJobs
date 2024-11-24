from typing import List, Dict, Any
from .models import QueryResponse
from .generator import generate_response
from .retriever import get_relevant_contexts
from ..config import Settings

def process_query(query: str, settings: Settings) -> QueryResponse:
    # Get relevant contexts
    contexts = get_relevant_contexts(query, settings)
    
    # Generate response
    response_text = generate_response(query, contexts, settings)
    
    # Return response
    return QueryResponse(
        text=response_text,
        contexts=[match['metadata']['text'] for match in contexts]
    )