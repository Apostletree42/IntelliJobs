from fastapi import HTTPException, status
from typing import Dict, Optional
from datetime import datetime
from jose import jwt

from .database import users_collection
from .models import UserModel
from .utils import get_password_hash, verify_password, create_access_token, create_refresh_token
from .schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from ..config import settings

import logging

logger = logging.getLogger(__name__)

async def get_user(email: str) -> Optional[UserModel]:
    """
    Retrieve a user by email
    """
    user_doc = await users_collection.find_one({"email": email})
    return UserModel(**user_doc) if user_doc else None

async def register_user(user: UserCreate) -> UserResponse:
    """
    Register a new user with comprehensive checks
    """
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    try:
        # Create user model with hashed password
        user_doc = UserModel(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            created_at=datetime.utcnow()
        )
        
        # Insert user into database
        result = await users_collection.insert_one(user_doc.dict(by_alias=True))
        
        # Fetch the created user to return complete data
        created_user = await users_collection.find_one({"_id": result.inserted_id})
        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User created but not found"
            )

        logger.info(f"User registered: {user.email}")
        
        return UserResponse(
            id=str(created_user["_id"]),
            email=created_user["email"],
            is_active=created_user["is_active"],
            created_at=created_user["created_at"]
        )
    
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )

async def login_user(user: UserLogin) -> TokenResponse:
    """
    Authenticate user and generate tokens
    """
    user_doc = await users_collection.find_one({"email": user.email})
    
    if not user_doc or not verify_password(user.password, user_doc["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Update last login
    await users_collection.update_one(
        {"email": user.email},
        {"$set": {"last_login": datetime.utcnow()}}
    )
    
    # Create tokens
    access_token = create_access_token({"sub": user.email})
    refresh_token = create_refresh_token({"sub": user.email})
    
    logger.info(f"User logged in: {user.email}")
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

async def refresh_tokens(refresh_token: str) -> TokenResponse:
    """
    Generate new access and refresh tokens
    """
    try:
        # Decode and validate refresh token
        payload = jwt.decode(
            refresh_token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        
        # Verify user exists
        user = await get_user(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Create new tokens
        new_access_token = create_access_token({"sub": email})
        new_refresh_token = create_refresh_token({"sub": email})
        
        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )