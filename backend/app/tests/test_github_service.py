import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime

from app.services.github_service import GitHubService
from app.models.schemas import TimeRange, Repository


class TestGitHubService:
    """Tests for GitHubService"""

    @pytest.mark.asyncio
    async def test_get_user_info_success(self, mock_github_user_response):
        """Test successful user info retrieval"""
        service = GitHubService()

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_github_user_response
            mock_response.raise_for_status = MagicMock()

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            result = await service.get_user_info("testuser")

            assert result["login"] == "testuser"
            assert result["id"] == 12345

    @pytest.mark.asyncio
    async def test_get_user_info_not_found(self):
        """Test user not found"""
        service = GitHubService()

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 404

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            with pytest.raises(ValueError, match="User .* not found"):
                await service.get_user_info("nonexistent")

    @pytest.mark.asyncio
    async def test_get_user_repos_success(self, mock_github_repos_response):
        """Test successful repos retrieval"""
        service = GitHubService()

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_github_repos_response
            mock_response.raise_for_status = MagicMock()

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            result = await service.get_user_repos("testuser")

            assert len(result) == 2
            assert isinstance(result[0], Repository)
            assert result[0].name == "test-repo-1"

    @pytest.mark.asyncio
    async def test_get_time_range_dates(self):
        """Test time range date calculation"""
        service = GitHubService()

        # Test day
        start, end = service._get_time_range_dates(TimeRange.DAY)
        assert (end - start).days == 1

        # Test week
        start, end = service._get_time_range_dates(TimeRange.WEEK)
        assert (end - start).days == 7

        # Test month
        start, end = service._get_time_range_dates(TimeRange.MONTH)
        assert (end - start).days == 30

        # Test year
        start, end = service._get_time_range_dates(TimeRange.YEAR)
        assert (end - start).days == 365

    @pytest.mark.asyncio
    async def test_get_repo_commits_success(self, mock_github_commits_response):
        """Test successful commits retrieval"""
        service = GitHubService()

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_github_commits_response
            mock_response.raise_for_status = MagicMock()

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            result = await service.get_repo_commits(
                "testuser",
                "test-repo",
                datetime(2024, 1, 1),
                datetime(2024, 1, 31),
                author="testuser"
            )

            assert len(result) == 2
            assert result[0]["sha"] == "abc123"

    @pytest.mark.asyncio
    async def test_get_authenticated_user(self):
        """Test authenticated user retrieval"""
        service = GitHubService(access_token="test_token")

        with patch("httpx.AsyncClient") as mock_client:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"login": "testuser"}
            mock_response.raise_for_status = MagicMock()

            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                return_value=mock_response
            )

            result = await service.get_authenticated_user()

            assert result["login"] == "testuser"

    @pytest.mark.asyncio
    async def test_get_authenticated_user_no_token(self):
        """Test authenticated user without token"""
        service = GitHubService()

        with pytest.raises(ValueError, match="Access token required"):
            await service.get_authenticated_user()

