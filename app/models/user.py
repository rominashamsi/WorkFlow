from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import base




class User(base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=True, nullable=False)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    password=Column(String,nullable=False)
    role=Column(String,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)


    projects=relationship("Project",back_populates="creator")
    tasks=relationship("Task",back_populates="assignee")
    comments=relationship("Comment",back_populates="user")
    project_members=relationship("ProjectMember",back_populates="user")

