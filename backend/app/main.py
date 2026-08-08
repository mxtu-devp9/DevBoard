from fastapi import FastAPI

from app.database.database import engine
from app.database.base import Base

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.projects import router as projects_router

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevBoard API",
    description="Project Management API",
    version="1.0.0"
)

# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(projects_router)



@app.get("/")
def root():
    return {
        "message": "Welcome to DevBoard API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "connected"
    }