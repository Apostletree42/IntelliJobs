from fastapi import HTTPException, status
from typing import Dict, Optional
from datetime import datetime
from jose import jwt

from .database import users_collection
from .models import User
from .utils import get_password_hash, verify_password, create_access_token, create_refresh_token
from .schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from ..config import settings

import logging

logger = logging.getLogger(__name__)

async def get_user_by_email_or_username(identifier: str) -> Optional[User]:
    """
    Retrieve a user by email or username
    """
    user_doc = await users_collection.find_one(
        {"$or": [{"email": identifier.lower()}, {"username": identifier}]}
    )
    return User(**user_doc) if user_doc else None

async def register_user(user: UserCreate) -> UserResponse:
    """
    Register a new user with comprehensive checks.
    """
    try:
        # Ensure email is lowercase
        user.email = user.email.lower()

        # Check if user already exists
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            logger.info(f"Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create user document with hashed password
        user_doc = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password),
            created_at=datetime.now(),
            is_active=True
        )

        # Insert user into database
        result = await users_collection.insert_one(user_doc.dict(by_alias=True))
        logger.debug(f"Inserted user ID: {result.inserted_id}")

        # Fetch the created user for response
        created_user = await users_collection.find_one({"_id": result.inserted_id})
        if not created_user:
            logger.error("User created but not found in database.")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User created but could not be retrieved."
            )

        logger.info(f"User registered successfully: {user.email}")
        return UserResponse(
            id=str(created_user["_id"]),
            email=created_user["email"],
            username=created_user["username"],  # Added this
            is_active=created_user.get("is_active", True),
            created_at=created_user["created_at"]
        )

    except ValueError as ve:
        # Handle password validation errors
        logger.error(f"Password validation failed: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException as e:
        # Rethrow known HTTP exceptions
        raise e
    except Exception as e:
        # Catch-all for unexpected errors
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to a server error."
        )

# Authenticate and login user
async def login_user(user: UserLogin) -> TokenResponse:
    """
    Authenticate user using email or username and generate tokens
    """
    # Get user from database using email or username
    db_user = await get_user_by_email_or_username(user.username_or_email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )

    # Verify password
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email/username or password"
        )

    # Generate tokens
    access_token = create_access_token({"sub": db_user.email})
    refresh_token = create_refresh_token({"sub": db_user.email})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

# Refresh tokens
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
        user = await get_user_by_email_or_username(email)
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