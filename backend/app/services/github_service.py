import httpx
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging

from app.config import settings
from app.models.schemas import (
    TimeRange, Repository, Commit, CommitActivity, UserActivity
)
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)


class GitHubService:
    """Service for interacting with GitHub API"""

    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.base_url = settings.GITHUB_API_BASE_URL
        self.graphql_url = settings.GITHUB_GRAPHQL_URL
        self.cache = CacheService()

        # Setup headers
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitPeek-App"
        }
        if access_token:
            self.headers["Authorization"] = f"token {access_token}"

    def _get_time_range_dates(self, time_range: TimeRange) -> tuple[datetime, datetime]:
        """Get start and end dates for time range"""
        end_date = datetime.utcnow()

        if time_range == TimeRange.DAY:
            start_date = end_date - timedelta(days=1)
        elif time_range == TimeRange.WEEK:
            start_date = end_date - timedelta(weeks=1)
        elif time_range == TimeRange.MONTH:
            start_date = end_date - timedelta(days=30)
        else:  # YEAR
            start_date = end_date - timedelta(days=365)

        return start_date, end_date

    async def get_user_info(self, username: str) -> Dict[str, Any]:
        """Get user information"""
        cache_key = f"user_info:{username}"

        # Try cache first
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users/{username}",
                headers=self.headers
            )

            if response.status_code == 404:
                raise ValueError(f"User {username} not found")

            response.raise_for_status()
            data = response.json()

            # Cache the result
            await self.cache.set(cache_key, data)
            return data

    async def get_user_repos(self, username: str, include_private: bool = False) -> List[Repository]:
        """Get user repositories"""
        cache_key = f"user_repos:{username}:{include_private}"

        # Try cache first
        cached = await self.cache.get(cache_key)
        if cached:
            return [Repository(**repo) for repo in cached]

        repos = []
        page = 1
        per_page = 100

        async with httpx.AsyncClient() as client:
            while True:
                params = {
                    "per_page": per_page,
                    "page": page,
                    "sort": "updated",
                    "direction": "desc"
                }

                # Use authenticated endpoint if token is available
                if self.access_token and include_private:
                    url = f"{self.base_url}/user/repos"
                else:
                    url = f"{self.base_url}/users/{username}/repos"

                response = await client.get(url, headers=self.headers, params=params)

                if response.status_code == 404:
                    break

                response.raise_for_status()
                data = response.json()

                if not data:
                    break

                repos.extend(data)

                # GitHub paginates at 100 per page
                if len(data) < per_page:
                    break

                page += 1

        # Convert to Repository models
        repo_models = [Repository(**repo) for repo in repos]

        # Cache the result
        await self.cache.set(cache_key, [repo.model_dump() for repo in repo_models])

        return repo_models

    async def get_repo_commits(
        self,
        owner: str,
        repo: str,
        since: datetime,
        until: datetime,
        author: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get commits for a repository within time range"""
        commits = []
        page = 1
        per_page = 100

        async with httpx.AsyncClient(timeout=30.0) as client:
            while True:
                params = {
                    "per_page": per_page,
                    "page": page,
                    "since": since.isoformat() + "Z",
                    "until": until.isoformat() + "Z"
                }

                if author:
                    params["author"] = author

                try:
                    response = await client.get(
                        f"{self.base_url}/repos/{owner}/{repo}/commits",
                        headers=self.headers,
                        params=params
                    )

                    if response.status_code == 409:  # Empty repository
                        break

                    if response.status_code == 404:
                        break

                    response.raise_for_status()
                    data = response.json()

                    if not data:
                        break

                    commits.extend(data)

                    if len(data) < per_page:
                        break

                    page += 1

                except httpx.HTTPError as e:
                    logger.error(f"Error fetching commits for {owner}/{repo}: {e}")
                    break

        return commits

    async def get_user_activity(
        self,
        username: str,
        time_range: TimeRange
    ) -> UserActivity:
        """Get user activity including repos and commits"""
        cache_key = f"user_activity:{username}:{time_range.value}:{self.access_token or 'public'}"

        # Try cache first
        cached = await self.cache.get(cache_key)
        if cached:
            return UserActivity(**cached)

        # Get time range
        start_date, end_date = self._get_time_range_dates(time_range)

        # Get user info
        user_info = await self.get_user_info(username)

        # Get repositories
        repos = await self.get_user_repos(username, include_private=bool(self.access_token))

        # Get commits from all repos
        all_commits: List[Commit] = []
        commit_dates: Dict[str, int] = {}

        for repo in repos[:50]:  # Limit to 50 most recent repos to avoid rate limits
            try:
                owner, repo_name = repo.full_name.split("/")
                commits_data = await self.get_repo_commits(
                    owner,
                    repo_name,
                    start_date,
                    end_date,
                    author=username
                )

                for commit_data in commits_data:
                    # Extract commit info
                    commit_info = commit_data.get("commit", {})
                    author_info = commit_info.get("author", {})

                    # Check if commit is by the user
                    if author_info.get("name") or author_info.get("email"):
                        commit_date_str = author_info.get("date", "")
                        if commit_date_str:
                            commit_date = datetime.fromisoformat(commit_date_str.replace("Z", "+00:00"))
                            date_key = commit_date.strftime("%Y-%m-%d")
                            commit_dates[date_key] = commit_dates.get(date_key, 0) + 1

                            commit = Commit(
                                sha=commit_data.get("sha", ""),
                                message=commit_info.get("message", "").split("\n")[0][:100],
                                author=author_info.get("name", username),
                                date=commit_date_str,
                                html_url=commit_data.get("html_url", ""),
                                repository=repo.full_name
                            )
                            all_commits.append(commit)

            except Exception as e:
                logger.error(f"Error processing repo {repo.full_name}: {e}")
                continue

        # Sort commits by date (newest first)
        all_commits.sort(key=lambda c: c.date, reverse=True)

        # Create activity chart
        activity_chart = [
            CommitActivity(date=date, count=count)
            for date, count in sorted(commit_dates.items())
        ]

        # Create user activity response
        activity = UserActivity(
            username=username,
            avatar_url=user_info.get("avatar_url"),
            total_commits=len(all_commits),
            repositories=repos[:20],  # Return top 20 repos
            commits=all_commits[:100],  # Return latest 100 commits
            activity_chart=activity_chart,
            time_range=time_range
        )

        # Cache the result
        await self.cache.set(cache_key, activity.model_dump())

        return activity

    async def get_authenticated_user(self) -> Dict[str, Any]:
        """Get authenticated user information"""
        if not self.access_token:
            raise ValueError("Access token required")

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/user",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

