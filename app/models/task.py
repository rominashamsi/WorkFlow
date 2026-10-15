
from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import base


class Task(base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)

    project_id = Column(
        Integer,
        ForeignKey("projects.id"),
        nullable=False,
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    assigned_to = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    deadline = Column(DateTime)
    created_at = Column(
    DateTime,
    default=lambda: datetime.now(UTC),
    ) 
    estimated_hours = Column(Integer)

    project = relationship(
        "Project",
        back_populates="tasks",
    )

    creator = relationship(
        "User",
        back_populates="created_tasks",
        foreign_keys=[created_by],
    )

    assignee = relationship(
        "User",
        back_populates="tasks",
        foreign_keys=[assigned_to],
    )

    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan",
    )

