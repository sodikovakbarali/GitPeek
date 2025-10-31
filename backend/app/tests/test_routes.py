import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from httpx import AsyncClient

from app.models.schemas import TimeRange


class TestPublicRoutes:
    """Tests for public API routes"""

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """Test root endpoint"""
        response = await client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """Test health check endpoint"""
        response = await client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_get_user_info_success(
        self,
        client: AsyncClient,
        mock_github_user_response
    ):
        """Test successful user info retrieval"""
        with patch("app.services.github_service.GitHubService.get_user_info") as mock:
            mock.return_value = mock_github_user_response

            response = await client.get("/api/public/user/testuser")

            assert response.status_code == 200
            data = response.json()
            assert data["login"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_user_info_not_found(self, client: AsyncClient):
        """Test user not found"""
        with patch("app.services.github_service.GitHubService.get_user_info") as mock:
            mock.side_effect = ValueError("User not found")

            response = await client.get("/api/public/user/nonexistent")

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_search_user(self, client: AsyncClient):
        """Test user search"""
        mock_activity = {
            "username": "testuser",
            "avatar_url": "https://example.com/avatar.jpg",
            "total_commits": 10,
            "repositories": [],
            "commits": [],
            "activity_chart": [],
            "time_range": "week"
        }

        with patch("app.services.github_service.GitHubService.get_user_activity") as mock:
            mock.return_value = MagicMock(**mock_activity)
            mock.return_value.model_dump = MagicMock(return_value=mock_activity)

            response = await client.get(
                "/api/public/search/testuser",
                params={"time_range": "week"}
            )

            assert response.status_code == 200


class TestAuthRoutes:
    """Tests for auth API routes"""

    @pytest.mark.asyncio
    async def test_github_login(self, client: AsyncClient):
        """Test GitHub login initiation"""
        response = await client.get("/api/auth/login")

        assert response.status_code == 200
        data = response.json()
        assert "auth_url" in data
        assert "github.com/login/oauth/authorize" in data["auth_url"]

    @pytest.mark.asyncio
    async def test_logout(self, client: AsyncClient):
        """Test logout"""
        with patch("app.services.auth_service.AuthService.delete_session") as mock:
            mock.return_value = True

            response = await client.post(
                "/api/auth/logout",
                headers={"Authorization": "Bearer test_session_id"}
            )

            assert response.status_code == 200
            data = response.json()
            assert "message" in data

    @pytest.mark.asyncio
    async def test_logout_no_auth(self, client: AsyncClient):
        """Test logout without authorization"""
        response = await client.post("/api/auth/logout")

        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_get_current_user(self, client: AsyncClient):
        """Test getting current user"""
        mock_session = MagicMock()
        mock_session.github_token = "test_token"

        with patch("app.services.auth_service.AuthService.get_session") as mock_get:
            with patch("app.services.github_service.GitHubService.get_authenticated_user") as mock_user:
                mock_get.return_value = mock_session
                mock_user.return_value = {"login": "testuser"}

                response = await client.get(
                    "/api/auth/me",
                    headers={"Authorization": "Bearer test_session_id"}
                )

                assert response.status_code == 200
                data = response.json()
                assert data["login"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_session(self, client: AsyncClient):
        """Test getting current user with invalid session"""
        with patch("app.services.auth_service.AuthService.get_session") as mock:
            mock.return_value = None

            response = await client.get(
                "/api/auth/me",
                headers={"Authorization": "Bearer invalid_session"}
            )

            assert response.status_code == 401

