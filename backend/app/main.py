from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.session import get_db
from app.core.redis import get_redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis import asyncio as aioredis
import logging

# Set up structured logging
setup_logging()
logger = logging.getLogger("app")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend service for MediOps AI Operations Platform",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", status_code=200)
async def health_check(
    db: AsyncSession = Depends(get_db),
    redis: aioredis.Redis = Depends(get_redis)
):
    """
    Health check endpoint to verify backend, database, and cache connectivity.
    """
    logger.info("Health check endpoint accessed")
    
    postgres_status = "unhealthy"
    redis_status = "unhealthy"
    
    # 1. Test PostgreSQL connectivity
    try:
        await db.execute(text("SELECT 1"))
        postgres_status = "healthy"
    except Exception as e:
        logger.error(f"PostgreSQL health check failed: {e}")
        
    # 2. Test Redis connectivity
    try:
        await redis.ping()
        redis_status = "healthy"
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")

    # Determine global health status
    if postgres_status != "healthy" or redis_status != "healthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "status": "unhealthy",
                "postgres": postgres_status,
                "redis": redis_status,
                "project_name": settings.PROJECT_NAME,
                "environment": settings.ENVIRONMENT,
            }
        )

    return {
        "status": "healthy",
        "postgres": postgres_status,
        "redis": redis_status,
        "project_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
    }
