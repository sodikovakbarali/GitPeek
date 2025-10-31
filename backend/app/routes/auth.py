from fastapi import APIRouter, HTTPException, Query, Header
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional

from app.config import settings
from app.models.schemas import (
    AuthResponse, UserActivity, TimeRange, UserActivityRequest
)
from app.services.auth_service import AuthService
from app.services.github_service import GitHubService

router = APIRouter()


@router.get("/login")
async def github_login(redirect_uri: Optional[str] = None):
    """
    Initiate GitHub OAuth login flow

    Redirects user to GitHub authorization page
    """
    # Use provided redirect_uri or default
    callback_uri = redirect_uri or settings.GITHUB_REDIRECT_URI

    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={callback_uri}"
        f"&scope=repo,user"
    )

    return {"auth_url": github_auth_url}


@router.get("/callback")
async def github_callback(code: str = Query(...)):
    """
    GitHub OAuth callback endpoint

    Exchanges authorization code for access token
    """
    if not settings.GITHUB_CLIENT_ID or not settings.GITHUB_CLIENT_SECRET:
        raise HTTPException(
            status_code=500,
            detail="GitHub OAuth not configured. Set GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET."
        )

    try:
        # Exchange code for access token
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                }
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to exchange code for token"
                )

            token_data = response.json()
            access_token = token_data.get("access_token")

            if not access_token:
                raise HTTPException(
                    status_code=400,
                    detail="No access token received"
                )

        # Get user info
        github_service = GitHubService(access_token)
        user_info = await github_service.get_authenticated_user()

        # Create session
        auth_service = AuthService()
        session_id = await auth_service.create_session(
            github_token=access_token,
            github_username=user_info["login"]
        )

        return AuthResponse(
            session_id=session_id,
            username=user_info["login"],
            avatar_url=user_info.get("avatar_url")
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Authentication error: {str(e)}"
        )


@router.post("/activity", response_model=UserActivity)
async def get_authenticated_activity(
    request: UserActivityRequest,
    authorization: Optional[str] = Header(None)
):
    """
    Get GitHub activity with authentication (includes private repos)

    Requires session ID in Authorization header: "Bearer {session_id}"
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )

    session_id = authorization.replace("Bearer ", "")

    # Get session
    auth_service = AuthService()
    session = await auth_service.get_session(session_id)

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    try:
        # Use authenticated GitHub service
        github_service = GitHubService(access_token=session.github_token)
        activity = await github_service.get_user_activity(
            request.username,
            request.time_range
        )
        return activity
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching activity: {str(e)}"
        )


@router.post("/logout")
async def logout(authorization: Optional[str] = Header(None)):
    """
    Logout user and delete session

    Requires session ID in Authorization header: "Bearer {session_id}"
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )

    session_id = authorization.replace("Bearer ", "")

    auth_service = AuthService()
    success = await auth_service.delete_session(session_id)

    if success:
        return {"message": "Logged out successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to logout")


@router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """
    Get current authenticated user information

    Requires session ID in Authorization header: "Bearer {session_id}"
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid authorization header"
        )

    session_id = authorization.replace("Bearer ", "")

    auth_service = AuthService()
    session = await auth_service.get_session(session_id)

    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    try:
        github_service = GitHubService(access_token=session.github_token)
        user_info = await github_service.get_authenticated_user()
        return user_info
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching user info: {str(e)}"
        )

