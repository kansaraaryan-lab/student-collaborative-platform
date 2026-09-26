from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.v1.router import api_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="Backend API for the Student Collaborative Platform",
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
         "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=[
        "GET",
        "POST",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
    "Content-Type",
    "Authorization",
    "X-User-ID",
],
)


@app.get("/")
async def root():
    return {
        "message": "Student Collaborative Platform API is running",
        "version": "0.1.0",
    }


app.include_router(api_router)