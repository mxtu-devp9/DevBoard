from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectResponse

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