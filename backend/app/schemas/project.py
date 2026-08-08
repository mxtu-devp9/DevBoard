from pydantic import BaseModel
from datetime import datetime


class ProjectBase(BaseModel):
    title: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: int
    status: str
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True