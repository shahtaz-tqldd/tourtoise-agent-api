from typing import Any, Dict, Optional


class APIError(Exception):
    """Base API exception"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class BadRequestError(APIError):
    """400 Bad Request"""
    
    def __init__(self, message: str = "Bad request", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=400, message=message, details=details)


class UnauthorizedError(APIError):
    """401 Unauthorized"""
    
    def __init__(self, message: str = "Unauthorized", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=401, message=message, details=details)


class ForbiddenError(APIError):
    """403 Forbidden"""
    
    def __init__(self, message: str = "Forbidden", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=403, message=message, details=details)


class NotFoundError(APIError):
    """404 Not Found"""
    
    def __init__(self, message: str = "Resource not found", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=404, message=message, details=details)


class ConflictError(APIError):
    """409 Conflict"""
    
    def __init__(self, message: str = "Resource conflict", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=409, message=message, details=details)


class UnprocessableEntityError(APIError):
    """422 Unprocessable Entity"""
    
    def __init__(self, message: str = "Unprocessable entity", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=422, message=message, details=details)


class InternalServerError(APIError):
    """500 Internal Server Error"""
    
    def __init__(self, message: str = "Internal server error", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=500, message=message, details=details)


class ServiceUnavailableError(APIError):
    """503 Service Unavailable"""
    
    def __init__(self, message: str = "Service unavailable", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=503, message=message, details=details)


# Database exceptions
class DatabaseError(APIError):
    """Database operation error"""
    
    def __init__(self, message: str = "Database error", details: Optional[Dict[str, Any]] = None):
        super().__init__(status_code=500, message=message, details=details)


class RecordNotFoundError(NotFoundError):
    """Database record not found"""
    
    def __init__(self, model: str, identifier: Any):
        super().__init__(
            message=f"{model} not found",
            details={"model": model, "identifier": str(identifier)}
        )


# Business logic exceptions
class ValidationError(BadRequestError):
    """Business validation error"""
    pass


class DuplicateError(ConflictError):
    """Duplicate resource error"""
    
    def __init__(self, resource: str, field: str, value: Any):
        super().__init__(
            message=f"{resource} with {field}='{value}' already exists",
            details={"resource": resource, "field": field, "value": str(value)}
        )