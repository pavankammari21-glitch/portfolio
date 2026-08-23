import json
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.experience import Experience
from app.models.user import User
from app.schemas.experience import ExperienceCreate, ExperienceOut
from app.schemas.common import StandardResponse
from app.dependencies import get_current_admin

router = APIRouter(prefix="/experience", tags=["Experience & Timeline"])

@router.get(
    "",
    response_model=StandardResponse[List[ExperienceOut]],
    summary="Get Experience, Education & Certifications Timeline",
    description="Retrieves structured timeline items ordered chronologically."
)
async def list_experience(
    item_type: Optional[str] = Query(None, description="Filter by 'work', 'education', or 'certification'"),
    db: Session = Depends(get_db)
):
    query = db.query(Experience)
    if item_type:
        query = query.filter(Experience.item_type == item_type.lower())
        
    items = query.order_by(Experience.order_index.asc()).all()
    return StandardResponse(
        success=True,
        message=f"Retrieved {len(items)} experience entries",
        data=[ExperienceOut.model_validate(exp) for exp in items]
    )

@router.post(
    "",
    response_model=StandardResponse[ExperienceOut],
    status_code=status.HTTP_201_CREATED,
    summary="Add Experience/Education (Admin Only)",
    description="Creates a new career history item."
)
async def create_experience(
    payload: ExperienceCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    achievements_str = json.dumps(payload.key_achievements) if isinstance(payload.key_achievements, list) else payload.key_achievements
    skills_str = json.dumps(payload.skills_used) if isinstance(payload.skills_used, list) else payload.skills_used

    exp = Experience(
        role_or_degree=payload.role_or_degree,
        organization=payload.organization,
        period=payload.period,
        location=payload.location,
        item_type=payload.item_type,
        description=payload.description,
        key_achievements=achievements_str,
        skills_used=skills_str,
        order_index=payload.order_index
    )
    db.add(exp)
    db.commit()
    db.refresh(exp)

    return StandardResponse(
        success=True,
        message="Experience item added successfully",
        data=ExperienceOut.model_validate(exp)
    )
