from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    assigned_to: int
    status: str = "todo"
    priority: str = "medium"
    deadline: datetime | None = None
    estimated_hours: int | None = Field(default=None, ge=0)


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    project_id: int
    assigned_to: int
    status: str
    priority: str
    deadline: datetime | None
    estimated_hours: int | None
    created_at: datetime


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    assigned_to: int | None = None
    status: str | None = None
    priority: str | None = None
    deadline: datetime | None = None
    estimated_hours: int | None = Field(default=None, ge=0)