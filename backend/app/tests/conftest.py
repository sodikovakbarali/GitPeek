import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from app.main import app
from app.database import Base, get_db


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True
)

# Test session maker
test_session_maker = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_maker() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
def mock_github_user_response():
    """Mock GitHub user response"""
    return {
        "login": "testuser",
        "id": 12345,
        "avatar_url": "https://avatars.githubusercontent.com/u/12345",
        "name": "Test User",
        "company": "Test Company",
        "blog": "https://testuser.com",
        "location": "Test City",
        "email": "test@example.com",
        "bio": "Test bio",
        "public_repos": 10,
        "followers": 100,
        "following": 50,
    }


@pytest.fixture
def mock_github_repos_response():
    """Mock GitHub repos response"""
    return [
        {
            "id": 1,
            "name": "test-repo-1",
            "full_name": "testuser/test-repo-1",
            "description": "Test repository 1",
            "private": False,
            "html_url": "https://github.com/testuser/test-repo-1",
            "language": "Python",
            "stargazers_count": 10,
            "forks_count": 5,
            "updated_at": "2024-01-01T00:00:00Z",
        },
        {
            "id": 2,
            "name": "test-repo-2",
            "full_name": "testuser/test-repo-2",
            "description": "Test repository 2",
            "private": False,
            "html_url": "https://github.com/testuser/test-repo-2",
            "language": "TypeScript",
            "stargazers_count": 20,
            "forks_count": 10,
            "updated_at": "2024-01-02T00:00:00Z",
        }
    ]


@pytest.fixture
def mock_github_commits_response():
    """Mock GitHub commits response"""
    return [
        {
            "sha": "abc123",
            "commit": {
                "message": "Test commit 1",
                "author": {
                    "name": "testuser",
                    "email": "test@example.com",
                    "date": "2024-01-01T12:00:00Z"
                }
            },
            "html_url": "https://github.com/testuser/test-repo-1/commit/abc123",
        },
        {
            "sha": "def456",
            "commit": {
                "message": "Test commit 2",
                "author": {
                    "name": "testuser",
                    "email": "test@example.com",
                    "date": "2024-01-02T12:00:00Z"
                }
            },
            "html_url": "https://github.com/testuser/test-repo-1/commit/def456",
        }
    ]

