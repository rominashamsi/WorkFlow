from datetime import datetime
from sqlalchemy import Column, Integer, String , ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.core.database import base


class Project(base):
    __tablename__="projects"
    id=Column(Integer, primary_key=True, index=True)
    name=Column(String,nullable=False)
    description=Column(String)
    created_by=Column(Integer,ForeignKey("users.id"),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)


    creator=relationship("User",back_populates="projects")
    members=relationship("ProjectMember",back_populates="project")
    tasks=relationship("Task",back_populates="project")

