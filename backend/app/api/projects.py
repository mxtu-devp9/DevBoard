from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


# ----------------------------
# Create Project
# ----------------------------
@router.post("/", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    new_project = Project(
        title=project.title,
        description=project.description,
        owner_id=1,
        status="Active"
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# ----------------------------
# Get All Projects
# ----------------------------
@router.get("/", response_model=list[ProjectResponse])
def get_projects(
    db: Session = Depends(get_db)
):
    projects = db.query(Project).all()
    return projects


# ----------------------------
# Get Project By ID
# ----------------------------
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    existing_project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not existing_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    existing_project.title = project.title
    existing_project.description = project.description

    db.commit()
    db.refresh(existing_project)

    return existing_project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully"
    }