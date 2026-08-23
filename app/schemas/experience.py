import json
from typing import Optional, List, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ExperienceBase(BaseModel):
    role_or_degree: str = Field(..., min_length=2, max_length=150)
    organization: str = Field(..., min_length=2, max_length=150)
    period: str = Field(..., min_length=2, max_length=100)
    location: str = Field("Hyderabad, India", max_length=100)
    item_type: str = Field("work", description="'work', 'education', or 'certification'")
    description: str = Field(..., min_length=10)
    key_achievements: Optional[Union[List[str], str]] = None
    skills_used: Optional[Union[List[str], str]] = None
    order_index: int = Field(0)

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role_or_degree: str
    organization: str
    period: str
    location: str
    item_type: str
    description: str
    key_achievements: List[str]
    skills_used: List[str]
    order_index: int

    @field_validator("key_achievements", mode="before")
    @classmethod
    def parse_achievements(cls, v):
        if not v:
            return []
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [line.strip("- ").strip() for line in v.split("\n") if line.strip()]
        return v

    @field_validator("skills_used", mode="before")
    @classmethod
    def parse_skills(cls, v):
        if not v:
            return []
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [s.strip() for s in v.split(",") if s.strip()]
        return v
