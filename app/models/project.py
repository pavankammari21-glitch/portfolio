import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False, index=True)
    slug = Column(String(150), unique=True, index=True, nullable=False)
    summary = Column(String(300), nullable=False)
    description = Column(Text, nullable=False)
    tech_stack = Column(String(500), nullable=False)  # Comma-separated or JSON list
    category = Column(String(50), default="Backend & Cloud", index=True)
    live_url = Column(String(300), nullable=True)
    github_url = Column(String(300), nullable=True)
    image_url = Column(String(300), nullable=True)
    architecture_notes = Column(Text, nullable=True)
    is_featured = Column(Boolean, default=True)
    stars_count = Column(Integer, default=48)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
