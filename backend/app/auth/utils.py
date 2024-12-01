from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
import re

from ..config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_password(password: str) -> str:
    """
    Validate password based on configuration rules and return validation error message if invalid
    """
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {settings.PASSWORD_MIN_LENGTH} characters long")
    
    if settings.PASSWORD_REQUIRE_UPPERCASE and not re.search(r'[A-Z]', password):
        raise ValueError("Password must contain at least one uppercase letter")
    
    if settings.PASSWORD_REQUIRE_LOWERCASE and not re.search(r'[a-z]', password):
        raise ValueError("Password must contain at least one lowercase letter")
    
    if settings.PASSWORD_REQUIRE_DIGITS and not re.search(r'\d', password):
        raise ValueError("Password must contain at least one digit")
    
    if settings.PASSWORD_REQUIRE_SPECIAL_CHARS and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValueError("Password must contain at least one special character")
    
    return password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a stored password against one provided by user
    """
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Hash the user's password
    """
    try:
        validated_password = validate_password(password)
        return pwd_context.hash(validated_password)
    except ValueError as e:
        raise ValueError(str(e))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token
    """
    return create_access_token(
        data, 
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )