from fastapi import APIRouter, Depends, HTTPException, status
from . import schemas, service

auth_router = APIRouter()

@auth_router.post("/register", response_model=schemas.UserResponse)
async def register_user(user: schemas.UserCreate):
    # Call the register_user function from the service
    return await service.register_user(user)

@auth_router.post("/login", response_model=schemas.TokenResponse)
async def login_user(user: schemas.UserLogin):
    # Call the login_user function from the service
    return await service.login_user(user)