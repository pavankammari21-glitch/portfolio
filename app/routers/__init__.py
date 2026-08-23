from app.routers.auth import router as auth_router
from app.routers.projects import router as projects_router
from app.routers.skills import router as skills_router
from app.routers.experience import router as experience_router
from app.routers.contact import router as contact_router
from app.routers.analytics import router as analytics_router
from app.routers.resume import router as resume_router
from app.routers.websocket import router as websocket_router

__all__ = [
    "auth_router",
    "projects_router",
    "skills_router",
    "experience_router",
    "contact_router",
    "analytics_router",
    "resume_router",
    "websocket_router"
]
