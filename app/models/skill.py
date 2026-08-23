from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(50), index=True, nullable=False)  # "Backend", "Databases", "DevOps & Cloud", "AI & ML", "Frontend"
    proficiency = Column(Integer, default=90)  # Percentage 1-100
    experience_years = Column(String(20), default="3+ years")
    icon = Column(String(100), default="⚡")
    is_primary = Column(Boolean, default=True)
