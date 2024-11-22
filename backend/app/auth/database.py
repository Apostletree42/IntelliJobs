from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings

client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client[settings.DATABASE_NAME]
users_collection = db["users"]