from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    role_or_degree = Column(String(150), nullable=False)
    organization = Column(String(150), nullable=False)
    period = Column(String(100), nullable=False)
    location = Column(String(100), default="Hyderabad, India")
    item_type = Column(String(50), default="work")  # "work", "education", "certification"
    description = Column(Text, nullable=False)
    key_achievements = Column(Text, nullable=True)  # JSON or newline-separated
    skills_used = Column(String(300), nullable=True)
    order_index = Column(Integer, default=0)
