from bson import ObjectId
from .models import User, UserCreate
from .utils import verify_password, get_password_hash
from .db import get_user_collection

async def get_user(username: str):
    collection = await get_user_collection()
    user_dict = await collection.find_one({"username": username})
    if user_dict:
        return User(**user_dict)
    return None

async def get_user_by_id(user_id: str):
    collection = await get_user_collection()
    user_dict = await collection.find_one({"_id": ObjectId(user_id)})
    if user_dict:
        return User(**user_dict)
    return None

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    collection = await get_user_collection()
    user_dict = user.model_dump()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    result = await collection.insert_one(user_dict)
    created_user = await get_user_by_id(str(result.inserted_id))
    return created_user