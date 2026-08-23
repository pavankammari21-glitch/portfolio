import sys
import time
import os
import platform
import fastapi
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sqlalchemy import text
from app.database import get_db
from app.models import Project, Skill, Experience, ContactMessage, User
from app.schemas.common import StandardResponse
from app.config import settings

router = APIRouter(prefix="/analytics", tags=["Analytics & System Telemetry"])

START_TIME = time.time()

@router.get(
    "/health",
    summary="Application Health & Readiness Probe",
    description="Kubernetes / Cloud provider ready healthcheck endpoint returning status and uptime."
)
async def health_check(db: Session = Depends(get_db)):
    db_status = "connected"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_status = "unreachable"

    uptime_seconds = int(time.time() - START_TIME)
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "database": db_status,
        "uptime_seconds": uptime_seconds,
        "uptime_formatted": f"{uptime_seconds // 3600}h {(uptime_seconds % 3600) // 60}m {uptime_seconds % 60}s"
    }

@router.get(
    "/overview",
    response_model=StandardResponse[dict],
    summary="Portfolio Metrics & Stats Overview",
    description="Aggregated platform statistics for the live frontend stats counters."
)
async def get_overview(db: Session = Depends(get_db)):
    projects_count = db.query(Project).count()
    skills_count = db.query(Skill).count()
    experience_count = db.query(Experience).count()
    inquiries_count = db.query(ContactMessage).count()

    return StandardResponse(
        success=True,
        message="Platform metrics retrieved successfully",
        data={
            "developer": {
                "name": settings.OWNER_NAME,
                "role": settings.OWNER_ROLE,
                "location": settings.OWNER_LOCATION,
                "github": settings.OWNER_GITHUB,
                "linkedin": settings.OWNER_LINKEDIN
            },
            "stats": {
                "total_projects": projects_count,
                "total_skills": skills_count,
                "career_milestones": experience_count,
                "inquiries_received": inquiries_count,
                "api_uptime_seconds": int(time.time() - START_TIME),
                "years_experience": "4+",
                "apis_engineered": "25+",
                "test_coverage_percent": "94%"
            },
            "environment": {
                "python_version": platform.python_version(),
                "fastapi_version": fastapi.__version__,
                "os": platform.system(),
                "architecture": platform.machine()
            }
        }
    )
