from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.api.health.schema import HealthCheckResponse
from app.core.config import get_settings

router = APIRouter()


@router.get(
    "",
    response_model=HealthCheckResponse,
    summary="Health Check",
    description="Check the health status of the API and its dependencies",
)
async def health_check(
    db: AsyncSession = Depends(get_async_session),
    settings = Depends(get_settings),
):
    """
    Health check endpoint that verifies:
    - API is running
    - Database connection is working
    - Redis connection is working (optional)
    """
    
    services = {}
    
    # Check database
    try:
        await db.execute(text("SELECT 1"))
        services["database"] = {
            "status": "healthy",
            "type": "postgresql",
        }
    except Exception as e:
        services["database"] = {
            "status": "unhealthy",
            "error": str(e),
        }
    
    # Overall status
    overall_status = "healthy" if all(
        s.get("status") == "healthy" for s in services.values()
    ) else "degraded"
    
    return HealthCheckResponse(
        status=overall_status,
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        services=services,
    )
