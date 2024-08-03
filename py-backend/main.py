from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Literal
from dotenv import load_dotenv
import os
import json
import torch
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from pinecone import Pinecone
from rag import process_query


load_dotenv()

class QueryRequest(BaseModel):
    text: str
    sender: Literal['user', 'bot']

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PINCONE_URI = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
GOOGLE_URI = os.getenv("GOOGLE_API_KEY")


@app.get("/ping")
async def ping():
    return "pong"

@app.post("/query")
async def query(request: QueryRequest):
    text = request.text

    if not text:
        raise HTTPException(status_code=400, detail="Invalid request, text is required")

    try:
        result = process_query(text, GOOGLE_URI, PINCONE_URI, PINECONE_INDEX)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3003)
