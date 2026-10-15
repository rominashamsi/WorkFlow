
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import base


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(
    DateTime,
    default=lambda: datetime.now(UTC),
    )

    projects = relationship("Project", back_populates="creator")

   
    tasks = relationship(
        "Task",
        back_populates="assignee",
        foreign_keys="Task.assigned_to",
    )

    
    created_tasks = relationship(
        "Task",
        back_populates="creator",
        foreign_keys="Task.created_by",
    )

    comments = relationship("Comment", back_populates="user")
    project_members = relationship("ProjectMember", back_populates="user")
