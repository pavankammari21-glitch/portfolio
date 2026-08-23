import time
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse

from app.config import settings
from app.database import engine, Base, SessionLocal
from app.services.seed_data import seed_initial_data
from app.exceptions import register_exception_handlers
from app.routers import (
    auth_router,
    projects_router,
    skills_router,
    experience_router,
    contact_router,
    analytics_router,
    resume_router,
    websocket_router
)

# --- 1. Lifespan Events (Modern FastAPI 0.93+) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and seed default portfolio data
    print("[STARTUP] Initializing database tables and models...")
    Base.metadata.create_all(bind=engine)
    
    with SessionLocal() as db:
        print("[STARTUP] Seeding default developer portfolio data & admin credentials...")
        seed_initial_data(db)
        
    print(f"[STARTUP] {settings.PROJECT_NAME} is live and ready!")
    yield
    # Shutdown: Clean up resources
    print("[SHUTDOWN] Application shutting down cleanly.")

# --- 2. FastAPI App Instantiation with Custom OpenAPI Metadata ---
tags_metadata = [
    {"name": "Health & Info", "description": "Core platform availability and metadata."},
    {"name": "Authentication & Security (OAuth2 & JWT)", "description": "OAuth2 password flow, JWT generation, and protected admin endpoints."},
    {"name": "Projects (CRUD, Filtering & File Uploads)", "description": "Full CRUD for developer projects, Query filters, Path parameters, and UploadFile."},
    {"name": "Skills & Tech Matrix", "description": "Technical skill proficiencies, categorized matrices, and levels."},
    {"name": "Experience & Timeline", "description": "Career history, academic milestones, and cloud certifications."},
    {"name": "Contact Inquiries & BackgroundTasks", "description": "Asynchronous email notifications, contact messages, and rate-limiting."},
    {"name": "Analytics & System Telemetry", "description": "Live uptime, health probes, and aggregate portfolio statistics."},
    {"name": "Dynamic Resume & Export (Headers/Cookies)", "description": "JSON Resume standard export, printable HTML/PDF, and custom cookie/header handling."},
    {"name": "Real-time WebSockets", "description": "Bidirectional WebSocket connection for live telemetry and visitor counter."}
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": f"{settings.OWNER_NAME} - Developer",
        "email": settings.ADMIN_EMAIL,
        "url": settings.OWNER_GITHUB
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# --- 3. Custom Middleware Pipeline ---
# A. CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# B. Custom Request Timing & Logging Middleware
@app.middleware("http")
async def add_process_time_and_log_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time-Sec"] = f"{process_time:.4f}"
    response.headers["X-Powered-By"] = "FastAPI & Python 3.11"
    return response

# --- 4. Register Custom Exception Handlers ---
register_exception_handlers(app)

# --- 5. Mount API Routers ---
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(projects_router, prefix=settings.API_V1_STR)
app.include_router(skills_router, prefix=settings.API_V1_STR)
app.include_router(experience_router, prefix=settings.API_V1_STR)
app.include_router(contact_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(resume_router, prefix=settings.API_V1_STR)
app.include_router(websocket_router)

# --- 6. Mount Static Assets & Serve Frontend SPA ---
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", tags=["Health & Info"], response_class=HTMLResponse)
async def serve_spa():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>FastAPI Portfolio API is running. Go to <a href='/docs'>/docs</a></h1>")

@app.get("/api/health", tags=["Health & Info"])
async def root_health():
    return {"status": "online", "message": "FastAPI Portfolio Engine is running smoothly."}
