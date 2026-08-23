import datetime
import json
from typing import Optional, List, Union
from pydantic import BaseModel, Field, field_validator, ConfigDict

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=150, description="Project title")
    slug: Optional[str] = Field(None, max_length=150, description="URL-friendly identifier")
    summary: str = Field(..., min_length=10, max_length=300, description="Brief elevator pitch")
    description: str = Field(..., min_length=20, description="Full technical description")
    tech_stack: Union[List[str], str] = Field(..., description="List of technologies or comma-separated string")
    category: str = Field("Backend & Cloud", description="Project category")
    live_url: Optional[str] = Field(None, description="Live deployment URL")
    github_url: Optional[str] = Field(None, description="Source code repository")
    image_url: Optional[str] = Field(None, description="Thumbnail / preview image")
    architecture_notes: Optional[str] = Field(None, description="Architecture highlights and design patterns")
    is_featured: bool = Field(True, description="Whether to feature prominently")
    stars_count: int = Field(0, ge=0, description="GitHub or community star count")

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be blank")
        return v

    @field_validator("slug", mode="before")
    @classmethod
    def generate_slug_if_missing(cls, v, values):
        if not v:
            title = getattr(values, "data", {}).get("title", "") if hasattr(values, "data") else ""
            if title:
                return title.lower().replace(" ", "-").replace("/", "-")
        return v

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    tech_stack: Optional[Union[List[str], str]] = None
    category: Optional[str] = None
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    image_url: Optional[str] = None
    architecture_notes: Optional[str] = None
    is_featured: Optional[bool] = None
    stars_count: Optional[int] = None

class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    summary: str
    description: str
    tech_stack: List[str]
    category: str
    live_url: Optional[str] = None
    github_url: Optional[str] = None
    image_url: Optional[str] = None
    architecture_notes: Optional[str] = None
    is_featured: bool
    stars_count: int
    created_at: datetime.datetime

    @field_validator("tech_stack", mode="before")
    @classmethod
    def parse_tech_stack(cls, v):
        if isinstance(v, str):
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [t.strip() for t in v.split(",") if t.strip()]
        return v
