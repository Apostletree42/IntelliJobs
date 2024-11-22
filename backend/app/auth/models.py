from pydantic import BaseModel, Field, EmailStr, validator
from bson import ObjectId
from typing import Optional
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            try:
                return ObjectId(str(v))
            except:
                raise TypeError("Invalid ObjectId")
        return v

class BaseModelWithId(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UserModel(BaseModelWithId):
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    @validator('email')
    def validate_email(cls, v):
        # Add more sophisticated email validation if needed
        return v

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[datetime] = None

class TokenBlacklist(BaseModelWithId):
    token: str
    blacklisted_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime