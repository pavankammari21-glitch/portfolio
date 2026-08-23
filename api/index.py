import sys
import os

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app
from app.database import engine, Base, SessionLocal
from app.services.seed_data import seed_initial_data

# Ensure database tables and initial seed data exist for serverless functions
try:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_initial_data(db)
except Exception as e:
    print(f"[Vercel Startup DB Init]: {e}")

