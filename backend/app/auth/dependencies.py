# AUTH RELATED DEPENDENCIES (in this file, you write functions which access entities or resources outside the module. 
# For ex: db interaction to store new user, etc)

# more ideas: create access token, get current user, check if current user is admin, etc.

# basically functions which are not core to the module, but still needed

# TAKE THIS FILE LYT IF YOU DONT UNDERSTAND WHAT TO PUT HERE

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional

from ..config import settings
from .models import TokenData, UserModel
from .service import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    """
    Validate JWT token and retrieve current user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    """
    Ensure the user is active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

async def get_current_superuser(current_user: UserModel = Depends(get_current_active_user)) -> UserModel:
    """
    Ensure the user is a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized"
        )
    return current_user