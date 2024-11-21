# from pydantic import BaseModel, Field, ConfigDict
# from bson import ObjectId
# from typing import Any

# class PydanticObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate

#     @classmethod
#     def validate(cls, v):
#         if not isinstance(v, ObjectId):
#             raise TypeError('ObjectId required')
#         return str(v)

#     @classmethod
#     def __get_pydantic_json_schema__(cls, field_schema: Any) -> Any:
#         field_schema.update(type="string")
#         return field_schema

# class User(BaseModel):
#     id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
#     username: str
#     email: str
#     hashed_password: str
#     disabled: bool = False

#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str}
#     )

# class UserCreate(BaseModel):
#     username: str
#     email: str
#     password: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: str | None = None

from pydantic import BaseModel
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError("ObjectId required")
        return str(v)

class UserModel(BaseModel):
    id: PyObjectId = None
    email: str
    hashed_password: str

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}