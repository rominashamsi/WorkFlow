from fastapi import FastAPI
from app.core.database import engine, base
from app.models import User, Project, ProjectMember, Task, Comment

base.metadata.create_all(bind=engine)

app=FastAPI()


@app.get("/")
def home():
    return {"message": "Welcome to WorkFlow"}