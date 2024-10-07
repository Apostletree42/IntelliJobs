from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from auth.router import router as auth_router
from chatbot.router import router as chatbot_router
from rag.router import router as rag_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    app.state.settings = settings
    print(f"Application is starting with DATABASE_URL={settings.DATABASE_URL}")

    yield 

    # Shutdown tasks

    print("Application is shutting down.")

app = FastAPI(lifespan=lifespan)

settings = Settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])
app.include_router(rag_router, prefix="/rag", tags=["rag"])

@app.get("/ping")
async def ping():
    return "pong"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=3001, reload=True)