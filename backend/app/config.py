from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # GitHub OAuth
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_REDIRECT_URI: str = "http://localhost:5173/auth/callback"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./gitpeek.db"

    # Cache
    CACHE_EXPIRE_MINUTES: int = 10
    REDIS_URL: Optional[str] = None
    USE_REDIS: bool = False

    # API
    GITHUB_API_BASE_URL: str = "https://api.github.com"
    GITHUB_GRAPHQL_URL: str = "https://api.github.com/graphql"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

