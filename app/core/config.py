from functools import lru_cache
from typing import List, Literal, Dict, Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation"""
    
    # Application
    app_name: str = "Tourtoise Agent API"
    app_env: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = Field(default=True, description="Debug mode")
    port: int = Field(default=5000)
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    
    # API
    api_v1_prefix: str = "/api/v1"
    openapi_prefix: str = ""
    
    # CORS
    allowed_origins: List[str] = Field(default=["*"])
    allowed_methods: List[str] = Field(default=["*"])
    allowed_headers: List[str] = Field(default=["*"])
    allowed_credentials: bool = True
    
    # Security
    trusted_hosts: List[str] = Field(default=["*"])
    jwt_secret_key: str = Field(
        default="5ca7dab2bd66eea423de74e6bd7f7c67f19e9a8fee03ebb98d1505ddaf5db365"
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Database - PostgreSQL
    postgres_server: str = Field(default="localhost")
    postgres_port: int = Field(default=5432, ge=1, le=65535)
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")
    postgres_db: str = Field(default="tourtoise_db")
    postgres_pool_size: int = Field(default=10, ge=5, le=100)
    postgres_max_overflow: int = Field(default=10, ge=0, le=50)
    postgres_pool_timeout: int = Field(default=30, ge=10, le=60)
    postgres_pool_recycle: int = Field(default=3600, ge=300)
    adk_db: str = "adk_sessions"
    
    # Redis
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379, ge=1, le=65535)
    redis_db: int = Field(default=0, ge=0, le=15)
    redis_password: str | None = None
    
    # Celery
    celery_broker_url: str | None = None
    celery_result_backend: str | None = None
    celery_task_track_started: bool = True
    celery_task_time_limit: int = 300

    # Cloudinary
    cloudinary_cloud_name: str = None
    cloudinary_api_key: str = None
    cloudinary_api_secret: str = None

    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    @field_validator("debug", mode="before")
    @classmethod
    def set_debug_from_env(cls, v, info):
        """Set debug based on environment"""
        app_env = info.data.get("app_env", "dev")
        if v is None:
            return app_env == "dev"
        return v
    
    @field_validator("log_level", mode="before")
    @classmethod
    def set_log_level_from_env(cls, v, info):
        """Set log level based on environment"""
        if v is None:
            app_env = info.data.get("app_env", "dev")
            return "DEBUG" if app_env == "dev" else "INFO"
        return v.upper()
    
    @property
    def postgres_async_url(self) -> str:
        """PostgreSQL async connection URL"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def postgres_sync_url(self) -> str:
        """PostgreSQL sync connection URL (for Alembic & Celery)"""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.postgres_db}"
        )
    
    @property
    def adk_db_url(self) -> str:
        """PostgreSQL DB URL for ADK sessions"""
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_server}:{self.postgres_port}/{self.adk_db}"
        )
    
    @property
    def redis_url(self) -> str:
        """Redis connection URL"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def celery_broker_redis_url(self) -> str:
        """Celery broker URL (defaults to Redis)"""
        return self.celery_broker_url or self.redis_url
    
    @property
    def celery_result_redis_backend(self) -> str:
        """Celery result backend URL (defaults to Redis)"""
        return self.celery_result_backend or self.redis_url
    
    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "title": self.app_name,
            "version":"1.0.0",
            "app_env": self.app_env,
            "debug": self.debug,
            "api_prefix": self.api_v1_prefix,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url":f"{self.api_v1_prefix}/openapi.json" if self.debug else None,
            "docs_url":f"{self.api_v1_prefix}/docs" if self.debug else None,
            "redoc_url":f"{self.api_v1_prefix}/redoc" if self.debug else None,
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
