import redis
from redis import Redis

from src.api.dependencies.read_secret_manager import read_value
from src.core.config import settings


def get_redis_password() -> str:
    """Get Upstash Password From SecretManager."""
    return read_value(name="upstash-redis-rest-password")


def cache() -> Redis:
    """Definition redis instance."""

    return redis.Redis(
        host=settings.upstash_redis_rest_host,
        port=settings.upstash_redis_rest_port,
        password=get_redis_password(),
        ssl=True,
    )
