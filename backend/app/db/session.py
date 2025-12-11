"""
SIMBA Backend - Database Session Management

SQLAlchemy session factory and dependency injection.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.utils.logger import logger


# Create engine based on database URL
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite (async)
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        future=True,
    )
elif settings.DATABASE_URL.startswith("postgresql"):
    # PostgreSQL (async)
    # Convert sync URL to async (postgresql -> postgresql+asyncpg)
    async_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(
        async_url,
        echo=settings.DEBUG,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,
        max_overflow=20,
    )
else:
    raise ValueError(f"Unsupported database URL: {settings.DATABASE_URL}")


# Session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
)


# Dependency for FastAPI
async def get_db() -> Generator[AsyncSession, None, None]:
    """
    Dependency that provides async database session.

    Usage in FastAPI:
        @app.get("/")
        async def endpoint(db: AsyncSession = Depends(get_db)):
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


# Initialize database (create tables)
async def init_db():
    """Initialize database tables"""
    from app.db.base import Base
    from app.db.models import User, Assistant, Conversation, Message, Tool, ToolProvider, Document

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created successfully")


# Drop all tables (for testing)
async def drop_db():
    """Drop all database tables"""
    from app.db.base import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    logger.info("Database tables dropped")


# Close database connections
async def close_db():
    """Close database connections"""
    await engine.dispose()
    logger.info("Database connections closed")
