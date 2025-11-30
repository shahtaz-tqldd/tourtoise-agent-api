from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware

from app.core.config import get_settings
from app.core.exceptions import APIError
from app.middleware.logging import LoggingMiddleware
from app.middleware.timing import TimingMiddleware

from .exception_handler import (
    http_error_handler,
    http422_error_handler,
    api_error_handler,
    unhandled_exception_handler,
)


def register_middlewares(app: FastAPI) -> None:
    """Register all application middlewares in correct order"""
    settings = get_settings()
    
    # Timing middleware (outermost - measures total time)
    if settings.debug:
        app.add_middleware(TimingMiddleware)
    
    # Logging middleware
    app.add_middleware(LoggingMiddleware)
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=settings.allowed_credentials,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
        expose_headers=["X-Request-ID"],
    )
    
    # Trusted host middleware (security)
    if settings.trusted_hosts != ["*"]:
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=settings.trusted_hosts,
        )
    
    # GZip compression
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,  # Only compress responses > 1KB
    )


def register_exception_handlers(app: FastAPI):
    """Register all application exception handlers"""
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(RequestValidationError, http422_error_handler)
    app.add_exception_handler(APIError, api_error_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)