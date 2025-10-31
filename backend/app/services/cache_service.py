import json
from datetime import datetime, timedelta
from typing import Optional, Any
from sqlalchemy import select, delete
import logging

from app.config import settings
from app.database import async_session_maker, CachedResponse

logger = logging.getLogger(__name__)


class CacheService:
    """Service for caching API responses"""

    def __init__(self):
        self.expire_minutes = settings.CACHE_EXPIRE_MINUTES

    async def get(self, key: str) -> Optional[Any]:
        """Get cached value by key"""
        try:
            async with async_session_maker() as session:
                result = await session.execute(
                    select(CachedResponse).where(
                        CachedResponse.cache_key == key,
                        CachedResponse.expires_at > datetime.utcnow()
                    )
                )
                cached = result.scalar_one_or_none()

                if cached:
                    return json.loads(cached.response_data)

                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    async def set(self, key: str, value: Any) -> bool:
        """Set cached value with expiration"""
        try:
            async with async_session_maker() as session:
                expires_at = datetime.utcnow() + timedelta(minutes=self.expire_minutes)

                # Delete existing cache entry
                await session.execute(
                    delete(CachedResponse).where(CachedResponse.cache_key == key)
                )

                # Create new cache entry
                cached = CachedResponse(
                    cache_key=key,
                    response_data=json.dumps(value),
                    expires_at=expires_at
                )
                session.add(cached)
                await session.commit()

                return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete cached value"""
        try:
            async with async_session_maker() as session:
                await session.execute(
                    delete(CachedResponse).where(CachedResponse.cache_key == key)
                )
                await session.commit()
                return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    async def clear_expired(self) -> int:
        """Clear expired cache entries"""
        try:
            async with async_session_maker() as session:
                result = await session.execute(
                    delete(CachedResponse).where(
                        CachedResponse.expires_at <= datetime.utcnow()
                    )
                )
                await session.commit()
                return result.rowcount
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return 0

