from fastapi import FastAPI
from app.core.database import engine, base
from app.models import User, Project, ProjectMember, Task, Comment

from app.routers import users,projects, tasks, comments

base.metadata.create_all(bind=engine)

app=FastAPI(title="WorkFlow")





app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"]
)


app.include_router(
    tasks.router,
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"]
)

app.include_router(
    comments.router,
    prefix="/projects/{project_id}/tasks/{task_id}/comments",
    tags=["Comments"],
)



@app.get("/")
def home():
    return {"message": "Welcome to WorkFlow"}