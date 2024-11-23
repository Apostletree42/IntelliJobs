from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import Settings
from .auth.router import auth_router
# from app.chatbot.router import chatbot_router
# from app.rag.router import router as rag_router
from contextlib import asynccontextmanager
from .core.database import connect_to_mongodb, close_mongodb_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.mongodb_client, app.mongodb = await connect_to_mongodb()
    print(f"Connected to MongoDB at {settings.DATABASE_URL}")
    yield
    # Shutdown
    await close_mongodb_connection(app.mongodb_client)
    print("Disconnected from MongoDB")

app = FastAPI(lifespan=lifespan)

settings = Settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
# app.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])
# app.include_router(rag_router, prefix="/rag", tags=["rag"])

@app.get("/")
async def root():
    doc_count = await app.mongodb.your_collection.count_documents({})
    return {"message": f"Connected to MongoDB. Document count: {doc_count}"}

@app.get("/ping")
async def ping():
    return "pong"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=3001, reload=True)