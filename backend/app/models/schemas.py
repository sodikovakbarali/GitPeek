from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class TimeRange(str, Enum):
    """Time range options"""
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    YEAR = "year"


class Repository(BaseModel):
    """Repository model"""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    private: bool = False
    html_url: str
    language: Optional[str] = None
    stars: int = Field(alias="stargazers_count", default=0)
    forks: int = Field(alias="forks_count", default=0)
    updated_at: Optional[str] = None


class Commit(BaseModel):
    """Commit model"""
    sha: str
    message: str
    author: str
    date: str
    html_url: str
    repository: str


class CommitActivity(BaseModel):
    """Daily commit activity"""
    date: str
    count: int


class UserActivity(BaseModel):
    """User activity summary"""
    username: str
    avatar_url: Optional[str] = None
    total_commits: int
    repositories: List[Repository]
    commits: List[Commit]
    activity_chart: List[CommitActivity]
    time_range: TimeRange


class UserActivityRequest(BaseModel):
    """Request model for user activity"""
    username: str
    time_range: TimeRange = TimeRange.WEEK


class AuthResponse(BaseModel):
    """OAuth response model"""
    session_id: str
    username: str
    avatar_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
    status_code: int = 400

