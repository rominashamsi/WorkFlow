from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate, ProjectMemberCreate, ProjectMemberResponse

from app.core.security import get_current_user
from app.models.user import User
from app.models.project_member import ProjectMember

router = APIRouter()


@router.post ("/",response_model=ProjectResponse)
def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    existing_project = (
        db.query(Project)
        .filter(
            Project.name == project_data.name,
            Project.created_by == current_user.id,
        )
        .first()
    )

    if existing_project:
        raise HTTPException(
            status_code=400,
            detail="You already have a project with this name",
        )





    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        created_by=current_user.id,
    )

    db.add(new_project)
    db.flush()

    new_member = ProjectMember(
        project_id=new_project.id,
        user_id=current_user.id,
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_project)

    return new_project


@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    projects = db.query(Project).all()
    return projects



@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_data: ProjectUpdate,  #Request_Body
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()  #model_instance
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own projects")
    
    if project_data.name is not None:
        project.name = project_data.name  # Update the project name with the value from the request body
    if project_data.description is not None:
        project.description = project_data.description
    db.commit()
    db.refresh(project)

    return project



@router.delete("/{project_id}")
def delete_project(
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

    if project.created_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own projects",
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }





@router.post("/{project_id}/members")
def add_project_member(
    project_id: int,
    member_data: ProjectMemberCreate,
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
            detail="Only the project creator can add members",
        )

    user = (
        db.query(User)
        .filter(User.id == member_data.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    existing_member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == member_data.user_id,
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this project",
        )

    new_member = ProjectMember(
        project_id=project_id,
        user_id=member_data.user_id,
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return {
        "message": "User added to project successfully",
        "project_id": project_id,
        "user_id": member_data.user_id,
    }    




@router.get("/{project_id}/members", response_model=list[ProjectMemberResponse])
def get_project_members(
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

    members = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id)
        .all()
    )

    result = []

    for member in members:
        user = (
            db.query(User)
            .filter(User.id == member.user_id)
            .first()
        )

        result.append({
            "id": member.id,
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })

    return result


@router.delete("/{project_id}/members/{user_id}")
def remove_project_member(
    project_id: int,
    user_id: int,
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
            detail="Only the project creator can remove members",
        )

    member = (
        db.query(ProjectMember)
        .filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == user_id,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="User is not a member of this project",
        )

    if user_id == project.created_by:
        raise HTTPException(
        status_code=400,
        detail="The project creator cannot be removed",
        )

    db.delete(member)
    db.commit()

    return {"message": "User removed from project successfully"}