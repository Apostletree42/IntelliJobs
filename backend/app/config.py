# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache
from datetime import timedelta
from typing import Dict, Any

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "rag_chatbot_db"
    
    # JWT Configuration
    JWT_SECRET: str = "your-very-secret-and-long-random-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Security Settings
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = True
    
    # RAG Configuration
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str
    GOOGLE_API_KEY: str
    
    # Model Settings
    EMBEDDING_MODEL_NAME: str = "BAAI/bge-small-en"
    EMBEDDING_MODEL_KWARGS: Dict[str, Any] = {"normalize_embeddings": True}
    
    # LLM Settings
    LLM_MODEL_NAME: str = "gemini-1.5-pro-latest"
    LLM_TEMPERATURE: float = 0.9
    LLM_TOP_K: int = 10
    
    # Cache Settings
    CACHE_TTL: int = 3600  # Time in seconds
    
    @property
    def access_token_expires(self) -> timedelta:
        return timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    @property
    def refresh_token_expires(self) -> timedelta:
        return timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    """
    Creates and returns a cached instance of the Settings.
    Using lru_cache ensures we don't create multiple instances
    unnecessarily.
    """
    return Settings()

# For backwards compatibility
settings = get_settings()