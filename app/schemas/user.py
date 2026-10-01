from datetime import datetime
from pydantic import BaseModel,Field,field_validator

class UserCreate(BaseModel):
    username: str=Field(min_length=3, max_length=50)
    first_name: str=Field(min_length=2, max_length=50)
    last_name: str=Field(min_length=2, max_length=50)
    password: str=Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    role: str
    created_at: datetime

   

class UserUpdate(BaseModel):
    first_name: str  | None=Field(default=None, min_length=2, max_length=50)
    last_name: str | None=Field(default=None, min_length=2, max_length=50)
