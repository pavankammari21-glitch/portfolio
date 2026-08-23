import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("portfolio.exceptions")

class PortfolioException(Exception):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, error_code: str = "BAD_REQUEST"):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(message)

class ResourceNotFoundException(PortfolioException):
    def __init__(self, resource_type: str, resource_id: str | int):
        super().__init__(
            message=f"{resource_type} with identifier '{resource_id}' was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND"
        )

class UnauthorizedException(PortfolioException):
    def __init__(self, detail: str = "Invalid credentials or token expired"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED"
        )

class PermissionDeniedException(PortfolioException):
    def __init__(self, detail: str = "You do not have permission to perform this action"):
        super().__init__(
            message=detail,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN"
        )

class RateLimitException(PortfolioException):
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message=f"Rate limit exceeded. Please retry in {retry_after} seconds.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED"
        )

def register_exception_handlers(app):
    @app.exception_handler(PortfolioException)
    async def portfolio_exception_handler(request: Request, exc: PortfolioException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.message,
                    "path": request.url.path
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = []
        for error in exc.errors():
            loc = " -> ".join([str(x) for x in error.get("loc", [])])
            errors.append({
                "field": loc,
                "msg": error.get("msg"),
                "type": error.get("type")
            })
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "The incoming payload failed Pydantic validation.",
                    "details": errors,
                    "path": request.url.path
                }
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": f"HTTP_{exc.status_code}",
                    "message": exc.detail,
                    "path": request.url.path
                }
            }
        )
