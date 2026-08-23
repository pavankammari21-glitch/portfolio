from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool = Field(True, description="Indicates if the request was successful")
    message: str = Field("Operation completed successfully", description="Status message")
    data: Optional[T] = Field(None, description="Payload data")

class PaginationMeta(BaseModel):
    total_items: int
    page: int
    limit: int
    total_pages: int
    has_next: bool
    has_prev: bool

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Data retrieved successfully"
    items: list[T]
    meta: PaginationMeta
