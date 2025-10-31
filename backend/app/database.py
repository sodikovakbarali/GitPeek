from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, DateTime, Text
from datetime import datetime

from app.config import settings


# Database engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class for database models"""
    pass


class CachedResponse(Base):
    """Model for caching GitHub API responses"""
    __tablename__ = "cached_responses"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String, unique=True, index=True, nullable=False)
    response_data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)


class UserSession(Base):
    """Model for storing user sessions"""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    github_token = Column(String, nullable=False)
    github_username = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency for getting database session"""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

