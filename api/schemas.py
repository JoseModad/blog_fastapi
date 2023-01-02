# Python

import os
import motor.motor_asyncio
from dotenv import load_dotenv
from bson import ObjectId

# Pydantic

from pydantic import BaseModel, Field, EmailStr

# Load env

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URL"))

db = client.blog_api


# Bson to fastapi JSON

class PyObjetcId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectID")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type = "string")
        
        
class User(BaseModel):
    id: PyObjetcId = Field(default_factory = PyObjetcId, alias = "_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    
    class Config:
        allowed_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jhon Doe",
                "email": "jdoe@example.com",
                "password": "secret-code"
            }
        }