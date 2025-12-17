from fastapi import APIRouter

from app.api.health.router import router as health_router 
from auth.router import router as auth_router
from destination.router import router as destination_router

# Main API router
api_router = APIRouter()

# Endpoint routers
api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

api_router.include_router(
    destination_router,
    prefix="/destinations",
    tags=["Destinations"],
)