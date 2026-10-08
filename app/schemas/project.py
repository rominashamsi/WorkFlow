from datetime import datetime
from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str | None = Field(default=None, max_length=500)




class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_by: int
    created_at: datetime



class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class ProjectMemberCreate(BaseModel):
    user_id: int


class ProjectMemberResponse(BaseModel):
    id: int
    user_id: int
    username: str
    first_name: str
    last_name: str