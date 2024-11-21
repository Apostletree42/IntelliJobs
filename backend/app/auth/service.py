from .database import users_collection
from .models import UserModel
from .utils import get_password_hash, verify_password, create_access_token  
from .schemas import UserCreate, UserLogin
from fastapi import HTTPException, status


async def register_user(user: UserCreate):
    user_doc = UserModel(email=user.email, hashed_password=get_password_hash(user.password))
    result = await users_collection.insert_one(user_doc.dict())
    return {"id": str(result.inserted_id), "email": user.email}

async def login_user(user: UserLogin):
    user_doc = await users_collection.find_one({"email": user.email})
    if not user_doc or not verify_password(user.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}