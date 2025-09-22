import json
import redis
from typing import Optional
from src.core.config import settings
from src.models.user import User

# Redis client
redis_client = redis.Redis.from_url(settings.redis_url)

def cache_user(user: User, expire_seconds: int = 300) -> None:
    """
    Cache user data in Redis for 5 minutes.
    
    Args:
        user: User object to cache
        expire_seconds: Cache expiration time 
    """
    key = f"user:{user.id}"
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_verified": user.is_verified,
        "avatar_url": user.avatar_url
    }
    redis_client.setex(key, expire_seconds, json.dumps(user_data))

def get_cached_user(user_id: int) -> Optional[dict]:
    """
    Get cached user data from Redis.
    
    Args:
        user_id: User's unique identifier
        
    Returns:
        User data dict or None
    """
    key = f"user:{user_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return None

def invalidate_user_cache(user_id: int) -> None:
    """
    Remove user from cache.
    
    Args:
        user_id: User's unique identifier
    """
    key = f"user:{user_id}"
    redis_client.delete(key)