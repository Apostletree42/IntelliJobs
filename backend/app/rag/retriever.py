from functools import lru_cache
import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from pinecone import Pinecone
from typing import List, Dict, Any
from ..config import Settings

@lru_cache()
def initialize_embeddings(model_name: str, **kwargs) -> HuggingFaceBgeEmbeddings:
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    return HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs={"device": device},
        encode_kwargs=kwargs
    )

@lru_cache()
def get_pinecone_client(api_key: str, index_name: str):
    return Pinecone(api_key=api_key).Index(index_name)

def get_relevant_contexts(query: str, settings: Settings) -> List[Dict[str, Any]]:
    embeddings = initialize_embeddings(
        settings.EMBEDDING_MODEL_NAME, 
        **settings.EMBEDDING_MODEL_KWARGS
    )
    pinecone_client = get_pinecone_client(
        settings.PINECONE_API_KEY,
        settings.PINECONE_INDEX_NAME
    )
    
    embedding = embeddings.embed_documents([query])[0]
    
    results = pinecone_client.query(
        namespace="job_data",
        vector=embedding,
        top_k=settings.LLM_TOP_K,
        include_values=True,
        include_metadata=True
    )
    
    return results['matches']