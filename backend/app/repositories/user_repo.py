"""
SIMBA Backend - User Repository

Repository for User model with custom queries.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        result = await self.db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def update_preferences(
        self,
        user_id: str,
        preferences: dict
    ) -> Optional[User]:
        """Update user preferences"""
        return await self.update(user_id, preferences=preferences)

    async def update_settings(
        self,
        user_id: str,
        settings: dict
    ) -> Optional[User]:
        """Update user settings"""
        return await self.update(user_id, settings=settings)
