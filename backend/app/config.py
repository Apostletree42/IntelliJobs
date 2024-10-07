# ALL GLOBAL CONFIG SETTINGS HERE

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://localhost:27017"
    JWT_SECRET: str = "your-secret-key"
    PINECONE_API_KEY: str = ''
    PINECONE_INDEX: str = ''
    GOOGLE_API_KEY: str = ''
    # Add other configuration variables as needed

    class Config:
        env_file = ".env"
