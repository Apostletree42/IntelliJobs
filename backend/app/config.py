# ALL GLOBAL CONFIG SETTINGS HERE

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # provided here are default values, pydantic will load these only if it cant find the .env file
    DATABASE_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "your_database_name"
    JWT_SECRET: str = "defaultKei"
    PINECONE_API_KEY: str = ''
    PINECONE_INDEX: str = ''
    GOOGLE_API_KEY: str = ''
    # Add other configuration variables as needed

    class Config:
        env_file = ".env"

