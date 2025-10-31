from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.models.schemas import (
    UserActivity, UserActivityRequest, TimeRange, ErrorResponse
)
from app.services.github_service import GitHubService

router = APIRouter()


@router.post("/activity", response_model=UserActivity)
async def get_user_activity(request: UserActivityRequest):
    """
    Get public GitHub activity for a user

    - **username**: GitHub username to query
    - **time_range**: Time range (day, week, month, year)
    """
    try:
        github_service = GitHubService()
        activity = await github_service.get_user_activity(
            request.username,
            request.time_range
        )
        return activity
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching user activity: {str(e)}"
        )


@router.get("/user/{username}")
async def get_user_info(username: str):
    """
    Get basic GitHub user information

    - **username**: GitHub username
    """
    try:
        github_service = GitHubService()
        user_info = await github_service.get_user_info(username)
        return user_info
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching user info: {str(e)}"
        )


@router.get("/search/{username}")
async def search_user(
    username: str,
    time_range: TimeRange = Query(TimeRange.WEEK)
):
    """
    Quick search for user activity

    - **username**: GitHub username
    - **time_range**: Time range (day, week, month, year)
    """
    try:
        github_service = GitHubService()
        activity = await github_service.get_user_activity(username, time_range)
        return activity
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching user: {str(e)}"
        )

