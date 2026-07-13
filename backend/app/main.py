from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
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
async def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    logger.info("Health check endpoint accessed")
    return {
        "status": "ok",
        "project_name": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
    }
