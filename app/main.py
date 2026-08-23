import time
import os
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

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
    try:
        Base.metadata.create_all(bind=engine)
        with SessionLocal() as db:
            print("[STARTUP] Seeding default developer portfolio data & admin credentials...")
            seed_initial_data(db)
    except Exception as e:
        print(f"[STARTUP DB INIT]: {e}")
        
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
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
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

# C. Vercel Serverless Path Normalizer Middleware
@app.middleware("http")
async def normalize_vercel_path(request: Request, call_next):
    import urllib.parse
    raw_path = request.scope.get("path", "")
    query_string = request.scope.get("query_string", b"").decode("utf-8")
    
    parsed_qs = urllib.parse.parse_qs(query_string, keep_blank_values=True)
    if "__route__" in parsed_qs:
        route_val = parsed_qs.pop("__route__")[0]
        request.scope["query_string"] = urllib.parse.urlencode(parsed_qs, doseq=True).encode("utf-8")
        target_path = "/" + route_val.lstrip("/") if route_val else "/"
        request.scope["path"] = target_path
        request.scope["raw_path"] = target_path.encode("utf-8")
    elif raw_path.startswith("/api/index.py") or raw_path.startswith("/api/index"):
        matched = (
            request.headers.get("x-vercel-matched-path")
            or request.headers.get("x-matched-path")
            or request.headers.get("x-invoke-path")
            or request.headers.get("x-forwarded-uri")
        )
        if matched and not (matched.startswith("/api/index.py") or matched.startswith("/api/index")):
            target_path = matched.split("?")[0]
        else:
            suffix = raw_path.replace("/api/index.py", "").replace("/api/index", "")
            target_path = suffix if suffix else "/"
        request.scope["path"] = target_path
        request.scope["raw_path"] = target_path.encode("utf-8")
            
    return await call_next(request)

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

@app.get("/static/{file_path:path}", include_in_schema=False)
async def serve_static_files(file_path: str):
    full_path = os.path.join(static_dir, file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        media_type = "text/plain"
        if file_path.endswith(".css"):
            media_type = "text/css"
        elif file_path.endswith(".js"):
            media_type = "application/javascript"
        elif file_path.endswith(".png"):
            media_type = "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            media_type = "image/jpeg"
        elif file_path.endswith(".svg"):
            media_type = "image/svg+xml"
        elif file_path.endswith(".html"):
            media_type = "text/html"

        with open(full_path, "rb") as f:
            return Response(
                content=f.read(),
                media_type=media_type,
                headers={"Cache-Control": "public, max-age=86400"}
            )
    raise HTTPException(status_code=404, detail="Static asset not found")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", tags=["Health & Info"], response_class=HTMLResponse)
@app.get("/api/index.py", include_in_schema=False, response_class=HTMLResponse)
@app.get("/api/index", include_in_schema=False, response_class=HTMLResponse)
async def serve_spa():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>FastAPI Portfolio API is running. Go to <a href='/docs'>/docs</a></h1>")

@app.get("/api/health", tags=["Health & Info"])
async def root_health():
    return {"status": "online", "message": "FastAPI Portfolio Engine is running smoothly."}

# Pre-serialize OpenAPI schema bytes at startup for zero runtime overhead
try:
    _cached_openapi_dict = app.openapi()
    _cached_openapi_json_bytes = json.dumps(_cached_openapi_dict).encode("utf-8")
except Exception as e:
    print(f"[OpenAPI Generation Warning]: {e}")
    _cached_openapi_dict = {}
    _cached_openapi_json_bytes = b"{}"

@app.get("/openapi.json", include_in_schema=False)
@app.get("/api/openapi.json", include_in_schema=False)
async def custom_openapi_json():
    global _cached_openapi_json_bytes
    if not _cached_openapi_json_bytes or _cached_openapi_json_bytes == b"{}":
        _cached_openapi_json_bytes = json.dumps(app.openapi()).encode("utf-8")
    return Response(
        content=_cached_openapi_json_bytes,
        media_type="application/json",
        headers={
            "Cache-Control": "public, max-age=3600",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.get("/api/debug/openapi", include_in_schema=False)
async def debug_openapi():
    import sys, traceback
    try:
        schema = app.openapi()
        return {
            "success": True,
            "paths_count": len(schema.get("paths", {})),
            "size": len(json.dumps(schema)),
            "python_version": sys.version
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@app.get("/docs", include_in_schema=False)
@app.get("/api/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=f"{settings.PROJECT_NAME} - Swagger UI",
        swagger_favicon_url="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>"
    )

@app.get("/redoc", include_in_schema=False)
@app.get("/api/redoc", include_in_schema=False)
async def custom_redoc_ui():
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title=f"{settings.PROJECT_NAME} - ReDoc"
    )
