import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "Pavan's Portfolio API & Platform"
    PROJECT_VERSION: str = "2.0.0"
    API_V1_STR: str = "/api"
    DESCRIPTION: str = (
        "🚀 Production-grade Developer Portfolio & Backend Service built with modern FastAPI. "
        "Showcasing full FastAPI capabilities including Async Lifespan, Pydantic V2 Validation, "
        "Dependency Injection, OAuth2 JWT Authentication, Background Tasks, WebSockets, "
        "SQLite Persistence, and Custom Middlewares."
    )
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "pavan_admin") or "pavan_admin"
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "fastapi_mastery_2026") or "fastapi_mastery_2026"
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "pavan.dev.engineer@gmail.com") if (os.getenv("ADMIN_EMAIL") and "@" in os.getenv("ADMIN_EMAIL", "")) else "pavan.dev.engineer@gmail.com"
    
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super-secret-fastapi-jwt-key-change-in-prod-0987654321")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:////tmp/portfolio.db" if (
            os.getenv("VERCEL")
            or os.getenv("VERCEL_ENV")
            or os.getenv("AWS_LAMBDA_FUNCTION_NAME")
            or os.getenv("LAMBDA_TASK_ROOT")
        ) else "sqlite:///./portfolio.db"
    )
    ALLOWED_ORIGINS: list[str] = ["*"]
    
    # Portfolio owner info
    OWNER_NAME: str = "Pavan"
    OWNER_ROLE: str = "Senior Full-Stack & Python / FastAPI Specialist"
    OWNER_TAGLINE: str = "Architecting resilient APIs, distributed backend systems, and modern AI-driven cloud web applications."
    OWNER_LOCATION: str = "Hyderabad, India / Remote"
    OWNER_GITHUB: str = "https://github.com"
    OWNER_LINKEDIN: str = "https://linkedin.com"

settings = Settings()
