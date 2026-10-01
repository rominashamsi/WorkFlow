from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import base


class ProjectMember(base):
    __tablename__="project_members"
    id=Column(Integer, primary_key=True, index=True)
    project_id=Column(Integer,ForeignKey("projects.id"),nullable=False)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)


    project=relationship("Project",back_populates ="members")
    user=relationship("User",back_populates="project_members")
