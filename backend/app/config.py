from pydantic_settings import BaseSettings
from datetime import timedelta

class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "rag_chatbot_db"

    # JWT Configuration
    JWT_SECRET: str = "your-very-secret-and-long-random-key"  # Replace with a strong secret
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Security Settings
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = True

    # External Service Keys
    PINECONE_API_KEY: str = ''
    PINECONE_INDEX: str = ''
    GOOGLE_API_KEY: str = ''

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()