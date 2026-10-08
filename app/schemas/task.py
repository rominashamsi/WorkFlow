from pydantic import BaseModel, Field
from datetime import datetime



class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    assigned_to: int
    status: str = "to do"
    priority: str = "medium"
    deadline: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    project_id: int
    assigned_to: int
    status: str
    priority: str
    deadline: datetime | None
    created_at: datetime


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    assigned_to: int | None = None
    status: str | None = None
    priority: str | None = None
    deadline: datetime | None = None