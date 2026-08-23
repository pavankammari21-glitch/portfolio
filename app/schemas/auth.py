import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user_info: "UserOut"

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    is_admin: bool = False

class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "pavan_admin"})
    password: str = Field(..., min_length=6, json_schema_extra={"example": "fastapi_mastery_2026"})

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = "Pavan"
    admin_secret_key: str = Field(..., description="Secret key to authorize admin registration")

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    full_name: str
    is_admin: bool
    is_active: bool
    created_at: datetime.datetime

Token.model_rebuild()
