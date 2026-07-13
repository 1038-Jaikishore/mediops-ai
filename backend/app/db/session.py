from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from typing import AsyncGenerator

from sqlalchemy.pool import NullPool
import sys

# Create database engine
engine_kwargs = {}
if "pytest" in sys.modules or settings.ENVIRONMENT == "testing":
    engine_kwargs["poolclass"] = NullPool

engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False,
    future=True,
    pool_pre_ping=True,
    **engine_kwargs
)

# Async session factory
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection generator to yield active database sessions.
    """
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
