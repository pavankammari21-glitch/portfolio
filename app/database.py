from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

import os

# Safe URL parsing with fallback for Vercel / serverless runtimes
db_url = (settings.DATABASE_URL or "").strip()
if not db_url or not (db_url.startswith("sqlite") or db_url.startswith("postgresql") or db_url.startswith("mysql")):
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME") or os.getenv("LAMBDA_TASK_ROOT"):
        db_url = "sqlite:////tmp/portfolio.db"
    else:
        db_url = "sqlite:///./portfolio.db"

# SQLite configuration (check_same_thread=False is required for SQLite with multi-threading)
connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}

engine = create_engine(
    db_url,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    FastAPI Yield Dependency for managing database sessions.
    Automatically closes the session after the request finishes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
