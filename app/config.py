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
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "pavankammari6@gmail.com") if (os.getenv("ADMIN_EMAIL") and "@" in os.getenv("ADMIN_EMAIL", "")) else "pavankammari6@gmail.com"
    
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
    
    # Portfolio owner info (from verified resume)
    OWNER_NAME: str = "Kammari Pavan"
    OWNER_ROLE: str = "Python & FastAPI Backend Developer | ML & IT Engineer"
    OWNER_TAGLINE: str = "B.Tech IT graduate specializing in Python, FastAPI, REST APIs, MySQL, and Machine Learning systems."
    OWNER_LOCATION: str = "Telangana, India"
    OWNER_PHONE: str = "7702189098"
    OWNER_GITHUB: str = "https://github.com/pavankammari6-wq"
    OWNER_LINKEDIN: str = "https://www.linkedin.com/in/pavan-kammari-352b18254/"

settings = Settings()
