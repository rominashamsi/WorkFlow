from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.models.project import Project
from app.models.project_member import ProjectMember
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.security import get_current_user


router = APIRouter()





@router.post("/", response_model=TaskResponse)
def create_task(
    project_id: int,
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    is_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
        )
        .first()
    )

    
    if is_member is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project",
    )

    assigned_user = (
        db.query(User)
        .filter(User.id == task_data.assigned_to) # "assigned_to" comes from the request body through the TaskCreate schema
        .first()
    )

    if assigned_user is None:
        raise HTTPException(
            status_code=404,
            detail="Assigned user not found",
        )

    assigned_user_is_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == task_data.assigned_to,
        )
        .first()
    )

    if assigned_user_is_member is None:
        raise HTTPException(
            status_code=400,
            detail="Assigned user is not a member of this project",
    )

    new_task = Task(
        title=task_data.title,
        description=task_data.description,   # "title" is the Task model field; "task_data.title" comes from the TaskCreate schema
        project_id=project_id,
        assigned_to=task_data.assigned_to,
        status=task_data.status,
        priority=task_data.priority,
        deadline=task_data.deadline,
        estimated_hours=task_data.estimated_hours,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/", response_model=list[TaskResponse])
def get_tasks(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    is_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
        )
        .first()
    )

    if project.created_by != current_user.id and is_member is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this project",
        )

    tasks = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )

    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    project_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    is_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id,
        )
        .first()
    )

    if is_member is None:
         raise HTTPException(
            status_code=403,
            detail="You are not a member of this project",
    )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    project_id: int,
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the project creator can update tasks",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.assigned_to is not None:
        assigned_user_is_member = (
            db.query(ProjectMember)
                       .filter(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == task_data.assigned_to,)
                        .first()
        )


        if assigned_user_is_member is None:
            raise HTTPException(
            status_code=400,
            detail="Assigned user is not a member of this project",
       )

        task.assigned_to = task_data.assigned_to

    if task_data.status is not None:
        task.status = task_data.status

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.deadline is not None:
        task.deadline = task_data.deadline


    if task_data.estimated_hours is not None:
        task.estimated_hours = task_data.estimated_hours

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}")
def delete_task(
    project_id: int,
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the project creator can delete tasks",
        )

    task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id,
        )
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}