from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, EmailStr, Field, GetJsonSchemaHandler
from bson import ObjectId
from pydantic_core import CoreSchema, core_schema
from typing_extensions import Annotated


# NOTE: a discrepancy here is, im using pydantic for data models in auth but beanie in rag
class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetJsonSchemaHandler,
    ) -> CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.str_schema(),
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x),
            ),
        )

class BaseModelWithId(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

class User(BaseModelWithId):  # Renamed from UserModel to User
    email: EmailStr
    username: str  # Added username field
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    @classmethod
    def validate_email(cls, email: str) -> str:
        # Add more sophisticated email validation if needed
        return email

class TokenData(BaseModel):
    username: Optional[str] = None
    exp: Optional[datetime] = None