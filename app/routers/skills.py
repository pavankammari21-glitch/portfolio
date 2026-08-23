from typing import Optional, List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.skill import Skill
from app.models.user import User
from app.schemas.skill import SkillCreate, SkillOut, CategorizedSkills
from app.schemas.common import StandardResponse
from app.dependencies import get_current_admin
from app.exceptions import PortfolioException

router = APIRouter(prefix="/skills", tags=["Skills & Tech Matrix"])

@router.get(
    "",
    response_model=StandardResponse[List[SkillOut]],
    summary="List All Skills",
    description="Returns flat list of technical proficiencies with optional category filtering."
)
async def list_skills(
    category: Optional[str] = Query(None, description="Filter skills by category (e.g. Backend, Databases, AI & ML)"),
    db: Session = Depends(get_db)
):
    query = db.query(Skill)
    if category:
        query = query.filter(Skill.category.ilike(f"%{category}%"))
        
    skills = query.order_by(Skill.proficiency.desc()).all()
    return StandardResponse(
        success=True,
        message=f"Found {len(skills)} skills",
        data=[SkillOut.model_validate(s) for s in skills]
    )

@router.get(
    "/categorized",
    response_model=StandardResponse[List[CategorizedSkills]],
    summary="List Skills Grouped by Category",
    description="Groups all skills into structured categories (Backend, Databases, DevOps, AI, Frontend) for matrix UI display."
)
async def list_categorized_skills(db: Session = Depends(get_db)):
    all_skills = db.query(Skill).order_by(Skill.proficiency.desc()).all()
    categories_dict: dict[str, list[SkillOut]] = {}

    for s in all_skills:
        cat = s.category
        if cat not in categories_dict:
            categories_dict[cat] = []
        categories_dict[cat].append(SkillOut.model_validate(s))

    result = [CategorizedSkills(category=k, skills=v) for k, v in categories_dict.items()]
    return StandardResponse(
        success=True,
        message="Grouped skills retrieved successfully",
        data=result
    )

@router.post(
    "",
    response_model=StandardResponse[SkillOut],
    status_code=status.HTTP_201_CREATED,
    summary="Add New Skill (Admin Only)",
    description="Creates a new skill entry."
)
async def create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    if db.query(Skill).filter(Skill.name.ilike(payload.name)).first():
        raise PortfolioException(f"Skill '{payload.name}' already exists", status_code=status.HTTP_409_CONFLICT)

    skill = Skill(
        name=payload.name,
        category=payload.category,
        proficiency=payload.proficiency,
        experience_years=payload.experience_years,
        icon=payload.icon,
        is_primary=payload.is_primary
    )
    db.add(skill)
    db.commit()
    db.refresh(skill)

    return StandardResponse(
        success=True,
        message=f"Skill '{skill.name}' added successfully",
        data=SkillOut.model_validate(skill)
    )
