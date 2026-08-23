import json
import os
import shutil
from typing import Optional, List
from fastapi import APIRouter, Depends, Query, Path, File, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectOut
from app.schemas.common import PaginatedResponse, PaginationMeta, StandardResponse
from app.dependencies import get_current_admin
from app.exceptions import ResourceNotFoundException, PortfolioException

router = APIRouter(prefix="/projects", tags=["Projects (CRUD, Filtering & File Uploads)"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get(
    "",
    response_model=PaginatedResponse[ProjectOut],
    summary="List Projects with Filtering & Pagination",
    description="Showcases FastAPI `Query` parameters: tech stack filtering, category filtering, search keyword, and pagination."
)
async def list_projects(
    tech: Optional[str] = Query(None, description="Filter by technology keyword (e.g., 'FastAPI', 'Docker', 'PostgreSQL')"),
    category: Optional[str] = Query(None, description="Filter by category (e.g. 'Backend & Cloud', 'AI & ML')"),
    search: Optional[str] = Query(None, min_length=2, description="Search query matching title, summary, or description"),
    featured_only: bool = Query(False, description="Return only featured flagship projects"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=50, description="Items per page"),
    db: Session = Depends(get_db)
):
    query = db.query(Project)

    if featured_only:
        query = query.filter(Project.is_featured == True)

    if category:
        query = query.filter(Project.category.ilike(f"%{category}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Project.title.ilike(search_pattern)) |
            (Project.summary.ilike(search_pattern)) |
            (Project.description.ilike(search_pattern))
        )

    all_items = query.order_by(Project.is_featured.desc(), Project.id.desc()).all()

    # In-memory filter for tech stack JSON
    if tech:
        tech_lower = tech.lower()
        filtered = []
        for p in all_items:
            try:
                stack = json.loads(p.tech_stack) if p.tech_stack.startswith("[") else [s.strip() for s in p.tech_stack.split(",")]
                if any(tech_lower in t.lower() for t in stack):
                    filtered.append(p)
            except Exception:
                pass
        all_items = filtered

    total_items = len(all_items)
    total_pages = max(1, (total_items + limit - 1) // limit)
    offset = (page - 1) * limit
    paginated_items = all_items[offset : offset + limit]

    return PaginatedResponse(
        success=True,
        message=f"Retrieved {len(paginated_items)} projects (Page {page} of {total_pages})",
        items=[ProjectOut.model_validate(p) for p in paginated_items],
        meta=PaginationMeta(
            total_items=total_items,
            page=page,
            limit=limit,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1
        )
    )

@router.get(
    "/{project_id}",
    response_model=StandardResponse[ProjectOut],
    summary="Get Project Details by ID",
    description="Showcases FastAPI `Path` parameter validation."
)
async def get_project(
    project_id: int = Path(..., ge=1, title="The Project ID", description="Integer ID of the project to retrieve"),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ResourceNotFoundException("Project", project_id)
        
    return StandardResponse(
        success=True,
        message="Project details retrieved successfully",
        data=ProjectOut.model_validate(project)
    )

@router.post(
    "",
    response_model=StandardResponse[ProjectOut],
    status_code=status.HTTP_201_CREATED,
    summary="Create New Project (Admin Only)",
    description="Requires Admin JWT Bearer authentication. Demonstrates Pydantic V2 body serialization and database persistence."
)
async def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    # Check slug collision
    slug = payload.slug or payload.title.lower().replace(" ", "-")
    if db.query(Project).filter(Project.slug == slug).first():
        slug = f"{slug}-{int(os.times().elapsed)}"

    tech_stack_json = json.dumps(payload.tech_stack) if isinstance(payload.tech_stack, list) else payload.tech_stack

    project = Project(
        title=payload.title,
        slug=slug,
        summary=payload.summary,
        description=payload.description,
        tech_stack=tech_stack_json,
        category=payload.category,
        live_url=str(payload.live_url) if payload.live_url else None,
        github_url=str(payload.github_url) if payload.github_url else None,
        image_url=str(payload.image_url) if payload.image_url else None,
        architecture_notes=payload.architecture_notes,
        is_featured=payload.is_featured,
        stars_count=payload.stars_count
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    return StandardResponse(
        success=True,
        message=f"Project '{project.title}' created successfully",
        data=ProjectOut.model_validate(project)
    )

@router.put(
    "/{project_id}",
    response_model=StandardResponse[ProjectOut],
    summary="Update Project (Admin Only)",
    description="Updates existing project details."
)
async def update_project(
    project_id: int = Path(..., ge=1),
    payload: ProjectUpdate = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ResourceNotFoundException("Project", project_id)

    update_data = payload.model_dump(exclude_unset=True)
    if "tech_stack" in update_data and isinstance(update_data["tech_stack"], list):
        update_data["tech_stack"] = json.dumps(update_data["tech_stack"])

    for field, val in update_data.items():
        setattr(project, field, val)

    db.commit()
    db.refresh(project)
    return StandardResponse(
        success=True,
        message="Project updated successfully",
        data=ProjectOut.model_validate(project)
    )

@router.delete(
    "/{project_id}",
    response_model=StandardResponse[dict],
    summary="Delete Project (Admin Only)",
    description="Deletes a project from the catalog."
)
async def delete_project(
    project_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ResourceNotFoundException("Project", project_id)

    db.delete(project)
    db.commit()
    return StandardResponse(
        success=True,
        message=f"Project ID {project_id} permanently removed.",
        data={"deleted_project_id": project_id}
    )

@router.post(
    "/{project_id}/thumbnail",
    response_model=StandardResponse[dict],
    summary="Upload Project Screenshot/Thumbnail (File Upload)",
    description="Showcases FastAPI `UploadFile` and `File(...)` multipart/form-data upload handling."
)
async def upload_project_thumbnail(
    project_id: int = Path(..., ge=1),
    file: UploadFile = File(..., description="Image file (.png, .jpg, .webp, .svg)"),
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ResourceNotFoundException("Project", project_id)

    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/svg+xml"]
    if file.content_type not in allowed_types:
        raise PortfolioException(f"Unsupported file type: {file.content_type}. Please upload a JPEG, PNG, WebP, or SVG.", status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    file_extension = os.path.splitext(file.filename)[1] or ".png"
    saved_filename = f"project_{project_id}_{int(os.times().elapsed)}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    relative_url = f"/static/uploads/{saved_filename}"
    project.image_url = relative_url
    db.commit()

    return StandardResponse(
        success=True,
        message="Project thumbnail uploaded successfully",
        data={"project_id": project_id, "image_url": relative_url}
    )
