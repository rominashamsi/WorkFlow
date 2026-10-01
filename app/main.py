from fastapi import FastAPI
from app.core.database import engine, base
from app.models import User, Project, ProjectMember, Task, Comment

from app.routers import users

base.metadata.create_all(bind=engine)

app=FastAPI()





app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

@app.get("/")
def home():
    return {"message": "Welcome to WorkFlow"}