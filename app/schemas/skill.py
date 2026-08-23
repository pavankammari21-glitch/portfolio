from typing import Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., description="E.g., Backend, Databases, DevOps & Cloud, AI & ML, Frontend")
    proficiency: int = Field(90, ge=1, le=100, description="Proficiency score from 1 to 100")
    experience_years: str = Field("3+ years", max_length=20)
    icon: str = Field("⚡", max_length=100)
    is_primary: bool = Field(True)

    @field_validator("category")
    @classmethod
    def normalize_category(cls, v: str) -> str:
        return v.strip().title()

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CategorizedSkills(BaseModel):
    category: str
    skills: list[SkillOut]
