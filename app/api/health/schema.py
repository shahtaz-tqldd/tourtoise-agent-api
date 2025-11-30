from pydantic import BaseModel, Field

class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str = Field(default="healthy")
    version: str = Field(default="1.0.0")
    timestamp: str
    services: dict = Field(default_factory=dict)
