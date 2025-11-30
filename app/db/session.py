import asyncio
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.db.base import Base

logger = setup_logging()
settings = get_settings()

# Async Engine (for FastAPI)
async_engine: AsyncEngine = create_async_engine(
    settings.postgres_async_url,
    echo=settings.debug,
    pool_size=settings.postgres_pool_size,
    max_overflow=settings.postgres_max_overflow,
    pool_timeout=settings.postgres_pool_timeout,
    pool_recycle=settings.postgres_pool_recycle,
    pool_pre_ping=True
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Sync Engine (for Celery & Alembic)
sync_engine = create_engine(
    settings.postgres_sync_url,
    echo=settings.debug,
    pool_size=settings.postgres_pool_size,
    max_overflow=settings.postgres_max_overflow,
    pool_timeout=settings.postgres_pool_timeout,
    pool_recycle=settings.postgres_pool_recycle,
    pool_pre_ping=True,
    connect_args={
        "connect_timeout": 10
    }
)

# Sync session factory
SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# Session Dependencies
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for async database sessions.
    
    Usage:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_async_session)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_session() -> Session:
    """
    Get sync session for Celery tasks.
    
    Usage (in Celery task):
        db = get_sync_session()
        try:
            # Your database operations
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
    """
    return SyncSessionLocal()


# Database Initialization
async def init_db(retries: int = 10, delay: int = 2) -> None:
    """
    Initialize database connection with retry logic.
    Useful for waiting for PostgreSQL to be ready in Docker.
    """
    logger.info(f"Attempting to connect to database")
    
    for attempt in range(1, retries + 1):
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("Database connection established!")
                return
                
        except Exception as e:
            logger.warning(
                f"Database connection attempt {attempt}/{retries} failed: {str(e)}"
            )
            logger.debug(f"Connection URL: postgresql://***:***@{settings.postgres_server}:{settings.postgres_port}/{settings.postgres_db}")
            await asyncio.sleep(delay)

    raise RuntimeError("Database initialization failed after retries")


def init_db_sync() -> None:
    """Initialize database tables synchronously (for scripts/testing)"""
    try:
        Base.metadata.create_all(bind=sync_engine)
        print("Database tables created successfully!")
    except Exception as e:
        print(f"Failed to create database tables: {e}")
        raise
            
async def close_db() -> None:
    """Close database connections gracefully"""
    try:
        await async_engine.dispose()
        logger.info("Async database connections closed")
    except Exception as e:
        logger.error(f"Error closing async database connections: {e}")
    
    try:
        sync_engine.dispose()
        logger.info("Sync database connections closed")
    except Exception as e:
        logger.error(f"Error closing sync database connections: {e}")
