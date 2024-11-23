from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., 
        min_length=8,
        description="Password must be at least 8 characters long"
    )

    @field_validator('password')
    def validate_password(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$', v):
            raise ValueError(
                'Password must contain at least one letter, one number, '
                'and be at least 8 characters long'
            )
        return v

    @field_validator('email')
    def lowercase_email(cls, v):
        return v.lower()

class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")

    @field_validator('email')
    def lowercase_email(cls, v):
        return v.lower()

class UserResponse(BaseModel):
    id: str = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    is_active: bool = Field(default=True, description="Whether the user account is active")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when the user was created"
    )

    class Config:
        json_encoders = {datetime: lambda dt: dt.isoformat()}
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(
        default=3600, 
        description="Token expiration time in seconds"
    )

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="New email address")
    is_active: Optional[bool] = Field(None, description="Account status")

    @field_validator('email')
    def lowercase_email(cls, v):
        if v is not None:
            return v.lower()
        return v

class PasswordChange(BaseModel):
    old_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ..., 
        min_length=8,
        description="New password must be at least 8 characters long"
    )

    @field_validator('new_password')
    def validate_new_password(cls, v):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$', v):
            raise ValueError(
                'New password must contain at least one letter, one number, '
                'and be at least 8 characters long'
            )
        return v

    @field_validator('new_password')
    def password_changed(cls, v, values):
        if 'old_password' in values and v == values['old_password']:
            raise ValueError('New password must be different from old password')
        return v