
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.database import engine, base
from app.models import User, Project, ProjectMember, Task, Comment
from app.routers import users, projects, tasks, comments


# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


base.metadata.create_all(bind=engine)

app = FastAPI(title="WorkFlow")


# Handle unexpected errors
@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        "Unexpected error while processing %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
        },
    )





app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"],
)

app.include_router(
    tasks.router,
    prefix="/projects/{project_id}/tasks",
    tags=["Tasks"],
)

app.include_router(
    comments.router,
    prefix="/projects/{project_id}/tasks/{task_id}/comments",
    tags=["Comments"],
)


@app.get("/")
def home():
    return {"message": "Welcome to WorkFlow"}
