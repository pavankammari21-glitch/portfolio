import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

class ContactCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, json_schema_extra={"example": "Elon Musk"})
    email: EmailStr = Field(..., json_schema_extra={"example": "elon@x.com"})
    subject: str = Field("Portfolio Inquiry", min_length=1, max_length=200, json_schema_extra={"example": "FastAPI Project Opportunity"})
    message: str = Field(..., min_length=2, max_length=3000, json_schema_extra={"example": "Hi Pavan, love your portfolio. Let's connect!"})

    @field_validator("name", "subject", "message")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field cannot be whitespace only")
        return v

class ContactOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    subject: str
    message: str
    client_ip: Optional[str] = None
    is_read: bool
    created_at: datetime.datetime

class ContactResponse(BaseModel):
    success: bool = True
    message: str
    inquiry_id: int
    estimated_response_time: str = "Within 24 hours"
