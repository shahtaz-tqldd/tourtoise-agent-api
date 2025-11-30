import traceback
from typing import Union
from pydantic import ValidationError

from fastapi import status
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.core.exceptions import APIError
from app.core.config import get_settings
from app.core.logging import setup_logging

logger = setup_logging()
settings = get_settings()


async def http_error_handler(_: Request, exc: HTTPException) -> JSONResponse:
    """Handle standard HTTP exceptions"""
    logger.warning(f"HTTP error: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
            "error_type": "http_error",
        },
    )


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    """Handle validation errors with improved formatting"""
    errors = exc.errors()
    
    # Extract field information
    validation_errors = []
    for error in errors:
        field_path = " -> ".join(str(loc) for loc in error["loc"][1:]) if len(error["loc"]) > 1 else "body"
        validation_errors.append({
            "field": field_path,
            "message": error["msg"],
            "type": error["type"],
        })
    
    # Create human-readable message
    if len(validation_errors) == 1:
        message = f"Validation error in '{validation_errors[0]['field']}': {validation_errors[0]['message']}"
    else:
        message = f"Validation failed for {len(validation_errors)} field(s)"
    
    logger.warning(f"Validation error: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": message,
            "error_type": "validation_error",
            "errors": validation_errors,
        },
    )


async def api_error_handler(_: Request, exc: APIError) -> JSONResponse:
    """Handle custom API errors"""
    logger.error(f"API error: {exc.status_code} - {exc.message}")
    
    content = {
        "success": False,
        "status_code": exc.status_code,
        "message": exc.message,
        "error_type": exc.__class__.__name__,
    }
    
    # Include details in debug mode or for client errors (4xx)
    if exc.details and (settings.debug or 400 <= exc.status_code < 500):
        content["details"] = exc.details
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    # Log full traceback
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}",
        exc_info=True,
    )
    
    content = {
        "success": False,
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        "message": "An unexpected error occurred. Please try again later.",
        "error_type": "internal_server_error",
    }
    
    # Include exception details only in debug mode
    if settings.debug:
        content["debug"] = {
            "exception_type": exc.__class__.__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc().split("\n"),
        }
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=content,
    )
