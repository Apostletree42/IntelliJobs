from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from . import schemas, service, dependencies
from .models import UserModel

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate):
    """
    Register a new user
    """
    return await service.register_user(user)

@auth_router.post("/login", response_model=schemas.TokenResponse)
async def login(user: schemas.UserLogin):
    """
    Authenticate and generate tokens
    """
    return await service.login_user(user)

@auth_router.post("/token/refresh", response_model=schemas.TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Generate new access and refresh tokens
    """
    return await service.refresh_tokens(refresh_token)

@auth_router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: UserModel = Depends(dependencies.get_current_active_user)):
    """
    Get current user profile
    """
    return schemas.UserResponse(
        id=str(current_user.id), 
        email=current_user.email
    )