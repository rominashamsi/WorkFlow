
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.routers import comments, projects, tasks, users

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




app = FastAPI(title="WorkFlow")


# Measure request processing time
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    import time

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        "%s %s completed in %.2f ms",
        request.method,
        request.url.path,
        process_time,
    )

    return response

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
