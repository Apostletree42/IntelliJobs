import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pinecone import Pinecone
from typing import List, Dict, Any
from ..config import Settings

def initialize_embeddings(settings: Settings) -> HuggingFaceBgeEmbeddings:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return HuggingFaceBgeEmbeddings(
        model_name=settings.EMBEDDING_MODEL_NAME,
        model_kwargs={"device": device},
        encode_kwargs=settings.EMBEDDING_MODEL_KWARGS
    )

def get_pinecone_client(settings: Settings):
    return Pinecone(api_key=settings.PINECONE_API_KEY).Index(settings.PINECONE_INDEX_NAME)

def get_relevant_contexts(query: str, settings: Settings) -> List[Dict[str, Any]]:
    # Initialize components (could be memoized if needed)
    embeddings = initialize_embeddings(settings)
    pinecone_client = get_pinecone_client(settings)
    
    # Get embedding for query
    embedding = embeddings.embed_documents([query])[0]
    
    # Query Pinecone
    results = pinecone_client.query(
        namespace="job_data",
        vector=embedding,
        top_k=settings.LLM_TOP_K,
        include_values=True,
        include_metadata=True
    )
    
    return results['matches']