from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import Token, UserLogin, UserRegister, UserOut
from app.services.auth_service import verify_password, get_password_hash, create_access_token
from app.dependencies import get_current_user
from app.exceptions import UnauthorizedException, PortfolioException
from app.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication & Security (OAuth2 & JWT)"])

@router.post(
    "/token",
    response_model=Token,
    summary="OAuth2 Password Flow Token Endpoint",
    description="Complies with OAuth2 specification. Allows authentication directly from the interactive Swagger /docs modal."
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise UnauthorizedException("Incorrect username or password")
        
    access_token = create_access_token(data={"sub": user.username, "is_admin": user.is_admin})
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info=UserOut.model_validate(user)
    )

@router.post(
    "/login",
    response_model=Token,
    summary="JSON Login Endpoint",
    description="Authenticates via standard JSON payload."
)
async def login_json(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise UnauthorizedException("Incorrect username or password")
        
    access_token = create_access_token(data={"sub": user.username, "is_admin": user.is_admin})
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info=UserOut.model_validate(user)
    )

@router.get(
    "/me",
    response_model=UserOut,
    summary="Get Current User Profile",
    description="Protected route demonstrating FastAPI Dependency Injection with OAuth2 Bearer token."
)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.post(
    "/register-admin",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register New Admin (Secret Key Protected)",
    description="Registers an admin account if provided with the valid master secret key."
)
async def register_admin(
    payload: UserRegister,
    db: Session = Depends(get_db)
):
    if payload.admin_secret_key != settings.JWT_SECRET_KEY:
        raise PortfolioException("Invalid admin secret key provided", status_code=status.HTTP_403_FORBIDDEN)
        
    if db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first():
        raise PortfolioException("User with this username or email already exists", status_code=status.HTTP_409_CONFLICT)
        
    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        full_name=payload.full_name,
        is_admin=True,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
