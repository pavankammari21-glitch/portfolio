import json
from typing import Optional
from fastapi import APIRouter, Depends, Response, Cookie, Header
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, Skill, Experience
from app.config import settings

router = APIRouter(prefix="/resume", tags=["Dynamic Resume & Export (Headers/Cookies)"])

@router.get(
    "/json",
    summary="Dynamic JSON Resume",
    description="Showcases JSON export adhering to the open-source JSON Resume schema specification."
)
async def get_json_resume(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    projects = db.query(Project).all()
    experiences = db.query(Experience).all()

    work_list = []
    education_list = []
    for exp in experiences:
        achievements = json.loads(exp.key_achievements) if exp.key_achievements and exp.key_achievements.startswith("[") else []
        item = {
            "name": exp.organization,
            "position": exp.role_or_degree,
            "startDate": exp.period,
            "summary": exp.description,
            "highlights": achievements
        }
        if exp.item_type == "education":
            education_list.append(item)
        else:
            work_list.append(item)

    resume_data = {
        "basics": {
            "name": settings.OWNER_NAME,
            "label": settings.OWNER_ROLE,
            "email": settings.ADMIN_EMAIL,
            "summary": settings.OWNER_TAGLINE,
            "location": {"city": "Hyderabad", "countryCode": "IN"},
            "profiles": [
                {"network": "GitHub", "url": settings.OWNER_GITHUB},
                {"network": "LinkedIn", "url": settings.OWNER_LINKEDIN}
            ]
        },
        "work": work_list,
        "education": education_list,
        "skills": [{"name": s.name, "level": f"{s.proficiency}%", "keywords": [s.category]} for s in skills],
        "projects": [{"name": p.title, "description": p.summary, "url": p.live_url or p.github_url} for p in projects]
    }
    return JSONResponse(content=resume_data)

@router.get(
    "/download",
    summary="Download Printable Resume (Demonstrates Custom Headers & Cookies)",
    description="Demonstrates setting custom response headers (`Content-Disposition`) and reading cookies."
)
async def download_resume_html(
    response: Response,
    visitor_preference: Optional[str] = Cookie(None, description="Optional cookie demonstration"),
    user_agent: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).all()
    projects = db.query(Project).filter(Project.is_featured == True).all()
    experiences = db.query(Experience).order_by(Experience.order_index.asc()).all()

    # Set response header and cookie demo
    response.set_cookie(key="last_resume_download", value="true", max_age=86400)
    response.headers["X-Portfolio-Engine"] = "FastAPI-v2"

    skills_html = "".join([
        f"<span style='display:inline-block;background:#1e293b;color:#38bdf8;padding:6px 12px;margin:4px;border-radius:6px;font-size:13px;font-weight:500;'>{s.name}</span>"
        for s in skills
    ])

    exp_html = ""
    for exp in experiences:
        achievements = json.loads(exp.key_achievements) if exp.key_achievements and exp.key_achievements.startswith("[") else []
        bullets = "".join([f"<li>{a}</li>" for a in achievements])
        exp_html += f"""
        <div style="margin-bottom: 20px;">
            <div style="display:flex; justify-content:space-between; align-items:baseline;">
                <h3 style="margin:0; color:#0f172a; font-size:16px;">{exp.role_or_degree} — <span style="color:#0284c7;">{exp.organization}</span></h3>
                <span style="font-size:13px; color:#64748b; font-weight:600;">{exp.period}</span>
            </div>
            <p style="margin:4px 0 6px 0; font-size:14px; color:#334155;">{exp.description}</p>
            <ul style="margin:4px 0 0 20px; font-size:13px; color:#475569;">
                {bullets}
            </ul>
        </div>
        """

    projects_html = ""
    for p in projects:
        stack = json.loads(p.tech_stack) if p.tech_stack.startswith("[") else [p.tech_stack]
        projects_html += f"""
        <div style="margin-bottom: 14px;">
            <div style="display:flex; justify-content:space-between;">
                <strong style="color:#0f172a; font-size:15px;">{p.title}</strong>
                <span style="font-size:12px; color:#0284c7;">{', '.join(stack)}</span>
            </div>
            <p style="margin:3px 0 0 0; font-size:13px; color:#475569;">{p.summary}</p>
        </div>
        """

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Pavan — Resume | FastAPI & Backend Specialist</title>
        <style>
            @media print {{
                body {{ padding: 0; background: #fff; }}
                .no-print {{ display: none !important; }}
            }}
            body {{
                font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                color: #1e293b;
                background: #f8fafc;
                margin: 0;
                padding: 40px 20px;
                line-height: 1.5;
            }}
            .resume-card {{
                max-width: 850px;
                margin: 0 auto;
                background: #ffffff;
                padding: 40px;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            }}
            h1 {{ margin: 0 0 4px 0; color: #0f172a; font-size: 28px; }}
            h2 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 24px; font-size: 18px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .btn-print {{
                position: fixed;
                top: 20px;
                right: 20px;
                background: #0284c7;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(2,132,199,0.3);
            }}
        </style>
    </head>
    <body>
        <button class="btn-print no-print" onclick="window.print()">🖨️ Print / Save as PDF</button>
        <div class="resume-card">
            <header style="border-bottom: 2px solid #0284c7; padding-bottom: 16px;">
                <h1>{settings.OWNER_NAME}</h1>
                <p style="margin: 4px 0; color: #0284c7; font-weight: 600; font-size: 16px;">{settings.OWNER_ROLE}</p>
                <div style="font-size: 13px; color: #64748b; margin-top: 6px;">
                    📍 {settings.OWNER_LOCATION} &nbsp;|&nbsp; ✉️ {settings.ADMIN_EMAIL} &nbsp;|&nbsp; 🌐 <a href="{settings.OWNER_GITHUB}" style="color:#0284c7;">GitHub</a> &nbsp;|&nbsp; 💼 <a href="{settings.OWNER_LINKEDIN}" style="color:#0284c7;">LinkedIn</a>
                </div>
            </header>

            <h2>Executive Summary</h2>
            <p style="font-size: 14px; color: #334155;">{settings.OWNER_TAGLINE}</p>

            <h2>Technical Expertise</h2>
            <div>{skills_html}</div>

            <h2>Education Qualification</h2>
            <div>{exp_html}</div>

            <h2>Featured Engineering Projects</h2>
            <div>{projects_html}</div>
        </div>
    </body>
    </html>
    """
    response_obj = HTMLResponse(content=html_content)
    response_obj.set_cookie(key="last_resume_download", value="true", max_age=86400)
    response_obj.headers["X-Portfolio-Engine"] = "FastAPI-v2"
    return response_obj
