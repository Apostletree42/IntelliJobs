import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone
import json

def process_query(query: str, google_api_key: str, pinecone_api_key: str, pinecone_index_name: str) -> str:
    # Initialize Pinecone
    pc = Pinecone(api_key=pinecone_api_key)
    index = pc.Index(pinecone_index_name)

    # Set up embeddings
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model_name = "BAAI/bge-small-en"
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}
    bge_embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )

    # Generate embedding for the query
    embed = bge_embeddings.embed_documents([query])
    user_embedding = embed[0]

    # Query Pinecone
    query_results = index.query(
        namespace="job_data",
        vector=user_embedding,
        top_k=10,
        include_values=True,
        include_metadata=True
    )

    # Extract contexts
    contexts = [match['metadata']['text'] for match in query_results['matches']]
    combined_context = '\n\n'.join(contexts)

    # Set up ChatGoogleGenerativeAI
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at answering questions based on a context extracted from a document. The context extracted from the document is: {context}"),
        ("human", "{question}"),
    ])
    llm = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model='gemini-1.5-pro-latest',
        temperature=0.9
    )
    chain = prompt | llm

    # Generate response
    response = chain.invoke({
        "context": combined_context,
        "question": query
    })

    # Prepare and return JSON response
    result = {
        "text": response.content,
        "sender": "bot"
    }
    return json.dumps(result)
