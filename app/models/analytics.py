import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base

class VisitorLog(Base):
    __tablename__ = "visitor_logs"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(255), nullable=True)
    path = Column(String(150), default="/")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
