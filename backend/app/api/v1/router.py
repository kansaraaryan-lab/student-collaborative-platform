from fastapi import APIRouter

from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.rooms import router as rooms_router
from backend.app.api.v1.students import router as students_router
from backend.app.api.v1.student_profiles import router as student_profiles_router
from backend.app.api.v1.skills import router as skills_router
from backend.app.api.v1.student_skills import (
    router as student_skills_router,
)

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(rooms_router)
api_router.include_router(students_router)
api_router.include_router(student_profiles_router)
api_router.include_router(skills_router)
api_router.include_router(student_skills_router)