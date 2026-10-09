from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import base


class Task(base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    deadline = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    estimated_hours = Column(Integer)

    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="tasks")

    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan",
    )