import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import select, delete
import logging

from app.config import settings
from app.database import async_session_maker, UserSession

logger = logging.getLogger(__name__)


class AuthService:
    """Service for handling authentication"""

    SESSION_EXPIRE_HOURS = 24 * 7  # 7 days

    async def create_session(
        self,
        github_token: str,
        github_username: str
    ) -> str:
        """Create a new user session"""
        try:
            session_id = secrets.token_urlsafe(32)
            expires_at = datetime.utcnow() + timedelta(hours=self.SESSION_EXPIRE_HOURS)

            async with async_session_maker() as session:
                user_session = UserSession(
                    session_id=session_id,
                    github_token=github_token,
                    github_username=github_username,
                    expires_at=expires_at
                )
                session.add(user_session)
                await session.commit()

            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise

    async def get_session(self, session_id: str) -> Optional[UserSession]:
        """Get session by ID"""
        try:
            async with async_session_maker() as session:
                result = await session.execute(
                    select(UserSession).where(
                        UserSession.session_id == session_id,
                        UserSession.expires_at > datetime.utcnow()
                    )
                )
                return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None

    async def delete_session(self, session_id: str) -> bool:
        """Delete a session"""
        try:
            async with async_session_maker() as session:
                await session.execute(
                    delete(UserSession).where(UserSession.session_id == session_id)
                )
                await session.commit()
                return True
        except Exception as e:
            logger.error(f"Error deleting session: {e}")
            return False

    async def clear_expired_sessions(self) -> int:
        """Clear expired sessions"""
        try:
            async with async_session_maker() as session:
                result = await session.execute(
                    delete(UserSession).where(
                        UserSession.expires_at <= datetime.utcnow()
                    )
                )
                await session.commit()
                return result.rowcount
        except Exception as e:
            logger.error(f"Error clearing sessions: {e}")
            return 0

