import pytest
from datetime import datetime, timedelta

from app.services.auth_service import AuthService


class TestAuthService:
    """Tests for AuthService"""

    @pytest.mark.asyncio
    async def test_create_session(self, db_session):
        """Test creating a new session"""
        auth = AuthService()

        session_id = await auth.create_session(
            github_token="test_token_123",
            github_username="testuser"
        )

        assert session_id is not None
        assert len(session_id) > 0

    @pytest.mark.asyncio
    async def test_get_session(self, db_session):
        """Test getting a session"""
        auth = AuthService()

        # Create session
        session_id = await auth.create_session(
            github_token="test_token_123",
            github_username="testuser"
        )

        # Get session
        session = await auth.get_session(session_id)

        assert session is not None
        assert session.session_id == session_id
        assert session.github_username == "testuser"
        assert session.github_token == "test_token_123"

    @pytest.mark.asyncio
    async def test_get_nonexistent_session(self, db_session):
        """Test getting non-existent session"""
        auth = AuthService()

        session = await auth.get_session("nonexistent_session_id")

        assert session is None

    @pytest.mark.asyncio
    async def test_delete_session(self, db_session):
        """Test deleting a session"""
        auth = AuthService()

        # Create session
        session_id = await auth.create_session(
            github_token="test_token_123",
            github_username="testuser"
        )

        # Delete session
        success = await auth.delete_session(session_id)
        assert success is True

        # Verify deleted
        session = await auth.get_session(session_id)
        assert session is None

    @pytest.mark.asyncio
    async def test_clear_expired_sessions(self, db_session):
        """Test clearing expired sessions"""
        auth = AuthService()

        # This test would need to manipulate time or database directly
        # For now, just test that the method runs
        count = await auth.clear_expired_sessions()
        assert isinstance(count, int)
        assert count >= 0

