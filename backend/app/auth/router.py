from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import logging
from . import schemas, service, dependencies
from .models import User

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate):
    """
    Register a new user.
    """
    try:
        return await service.register_user(user)
    except HTTPException as http_exc:
        # Return custom HTTP exceptions as is
        logger.error(f"HTTPException: {http_exc.detail}")
        raise http_exc
    except ValueError as ve:
        # Handle password validation errors specifically
        logger.error(f"Validation error during registration: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        # Log and return a generic internal server error
        logger.error(f"Unhandled error during registration: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration."
        )

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
async def read_users_me(current_user: User = Depends(dependencies.get_current_active_user)):
    """
    Get current user profile
    """
    return schemas.UserResponse(
        id=str(current_user.id), 
        email=current_user.email
    )