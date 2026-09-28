from fastapi import APIRouter

from backend.app.api.v1.health import router as health_router
from backend.app.api.v1.rooms import router as rooms_router
from backend.app.api.v1.students import router as students_router
from backend.app.api.v1.student_profiles import (
    router as student_profiles_router,
)
from backend.app.api.v1.skills import router as skills_router
from backend.app.api.v1.student_skills import (
    router as student_skills_router,
)
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.messages import router as messages_router
from backend.app.api.v1.messages_ws import router as messages_ws_router
from backend.app.api.v1.team_builder import router as team_builder_router
from backend.app.api.v1.events import router as events_router

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(health_router)
api_router.include_router(rooms_router)
api_router.include_router(students_router)
api_router.include_router(student_profiles_router)
api_router.include_router(skills_router)
api_router.include_router(student_skills_router)

# Authentication
api_router.include_router(auth_router)

# Messages
api_router.include_router(messages_router)
api_router.include_router(messages_ws_router)

# Team Builder
api_router.include_router(team_builder_router)

#Events
api_router.include_router(events_router)