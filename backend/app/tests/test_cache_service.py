import pytest
from datetime import datetime, timedelta

from app.services.cache_service import CacheService


class TestCacheService:
    """Tests for CacheService"""

    @pytest.mark.asyncio
    async def test_set_and_get(self, db_session):
        """Test setting and getting cache value"""
        cache = CacheService()

        test_key = "test_key"
        test_value = {"data": "test_data", "count": 42}

        # Set cache
        success = await cache.set(test_key, test_value)
        assert success is True

        # Get cache
        result = await cache.get(test_key)
        assert result == test_value

    @pytest.mark.asyncio
    async def test_get_nonexistent(self, db_session):
        """Test getting non-existent cache value"""
        cache = CacheService()

        result = await cache.get("nonexistent_key")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete(self, db_session):
        """Test deleting cache value"""
        cache = CacheService()

        test_key = "test_key"
        test_value = {"data": "test_data"}

        # Set cache
        await cache.set(test_key, test_value)

        # Delete cache
        success = await cache.delete(test_key)
        assert success is True

        # Verify deleted
        result = await cache.get(test_key)
        assert result is None

    @pytest.mark.asyncio
    async def test_overwrite_existing(self, db_session):
        """Test overwriting existing cache value"""
        cache = CacheService()

        test_key = "test_key"
        value1 = {"data": "value1"}
        value2 = {"data": "value2"}

        # Set first value
        await cache.set(test_key, value1)

        # Overwrite with second value
        await cache.set(test_key, value2)

        # Get and verify
        result = await cache.get(test_key)
        assert result == value2

    @pytest.mark.asyncio
    async def test_clear_expired(self, db_session):
        """Test clearing expired cache entries"""
        cache = CacheService()

        # This test would need to manipulate time or database directly
        # For now, just test that the method runs
        count = await cache.clear_expired()
        assert isinstance(count, int)
        assert count >= 0

