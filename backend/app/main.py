from fastapi import FastAPI

from backend.app.api.v1.router import api_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Student Collaborative Platform",
    version=settings.app_version,
)

@app.get("/")
async def root():
    return {
        "message": "Student Collaborative Platform API is running",
        "version": "0.1.0",
    }


app.include_router(api_router)