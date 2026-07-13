from redis import asyncio as aioredis
from app.core.config import settings

# Async Redis client
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True,
)


async def get_redis() -> aioredis.Redis:
    """
    Dependency injection generator to return the active Redis client.
    """
    return redis_client
