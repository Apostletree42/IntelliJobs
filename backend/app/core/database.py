# Mongodb connection setup
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import Settings

settings = Settings()

async def get_database():
    return AsyncIOMotorClient(settings.DATABASE_URL)[settings.DATABASE_NAME]

async def connect_to_mongodb():
    client = AsyncIOMotorClient(settings.DATABASE_URL)
    db = client[settings.DATABASE_NAME]
    return client, db

async def close_mongodb_connection(client):
    client.close()