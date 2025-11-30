from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.session import init_db, close_db
from app.middleware import (
    register_middlewares, 
    register_exception_handlers
)
from app.api.router import api_router

# Initialize logger
logger = setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting up application...")
    await init_db()
    logger.info("Database initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Application shutdown complete")


def create_application() -> FastAPI:
    """Application factory pattern"""
    settings = get_settings()
    
    app = FastAPI(**settings.fastapi_kwargs, lifespan=lifespan)
    
    # Register middlewares
    register_middlewares(app)

    # Register exception handlers
    register_exception_handlers(app)
    
    # Include API router
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    logger.info(f"Application initialized in {settings.app_env} mode")
    
    return app


app = create_application()
