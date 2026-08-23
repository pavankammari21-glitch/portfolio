import time
from typing import Optional
from fastapi import Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.auth_service import decode_access_token
from app.exceptions import UnauthorizedException, PermissionDeniedException, RateLimitException

# OAuth2 Password Bearer flow standard in FastAPI
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/token",
    auto_error=False,
    scheme_name="OAuth2PasswordBearer"
)

# Rate limiting storage for demonstration: {client_ip: [timestamp, timestamp, ...]}
RATE_LIMIT_STORAGE: dict[str, list[float]] = {}

def get_client_ip(request: Request, x_forwarded_for: Optional[str] = Header(None)) -> str:
    """
    Dependency: Extracts client IP supporting reverse proxies (Cloudflare, Nginx, Render, Railway).
    """
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "127.0.0.1"

def rate_limiter(max_requests: int = 15, window_seconds: int = 60):
    """
    Callable dependency factory for rate-limiting specific endpoints (e.g. contact form submissions).
    """
    def limiter(client_ip: str = Depends(get_client_ip)):
        now = time.time()
        requests = RATE_LIMIT_STORAGE.get(client_ip, [])
        # Filter out requests older than window_seconds
        valid_requests = [t for t in requests if now - t < window_seconds]
        
        if len(valid_requests) >= max_requests:
            raise RateLimitException(retry_after=int(window_seconds - (now - valid_requests[0])))
            
        valid_requests.append(now)
        RATE_LIMIT_STORAGE[client_ip] = valid_requests
        return True

    return limiter

async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency: Decodes JWT Bearer token and returns active User instance.
    """
    if not token:
        raise UnauthorizedException("Authentication token is required")
        
    payload = decode_access_token(token)
    if not payload or not payload.sub:
        raise UnauthorizedException("Could not validate credentials or token expired")
        
    user = db.query(User).filter(User.username == payload.sub).first()
    if not user:
        raise UnauthorizedException("User does not exist")
    if not user.is_active:
        raise UnauthorizedException("User account is inactive")
        
    return user

async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency: Ensures the authenticated user possesses administrative privileges.
    """
    if not current_user.is_admin:
        raise PermissionDeniedException("Administrative privileges required for this operation")
    return current_user
