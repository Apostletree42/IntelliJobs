from fastapi import APIRouter, Depends
from .service import AuthService
from .models import UserCreate, Token

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    return await auth_service.register(user)

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    return await auth_service.login(user)