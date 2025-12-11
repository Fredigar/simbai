"""
SIMBA Backend - Message Repository

Repository for Message model with custom queries.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Message, Assistant
from app.repositories.base import BaseRepository


class MessageRepository(BaseRepository[Message]):
    """Repository for Message operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)

    async def get_with_assistant(self, id: str) -> Optional[Message]:
        """Get message with assistant details"""
        result = await self.db.execute(
            select(Message)
            .options(selectinload(Message.assistant))
            .where(Message.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_conversation(
        self,
        conversation_id: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Message]:
        """Get messages for a conversation"""
        result = await self.db.execute(
            select(Message)
            .options(selectinload(Message.assistant))
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_latest_by_conversation(
        self,
        conversation_id: str,
        limit: int = 10
    ) -> List[Message]:
        """Get latest messages from conversation"""
        result = await self.db.execute(
            select(Message)
            .options(selectinload(Message.assistant))
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        return list(reversed(list(result.scalars().all())))

    async def get_by_role(
        self,
        conversation_id: str,
        role: str
    ) -> List[Message]:
        """Get messages by role"""
        result = await self.db.execute(
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.role == role
            )
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    async def count_by_role(
        self,
        conversation_id: str,
        role: str
    ) -> int:
        """Count messages by role"""
        from sqlalchemy import func

        result = await self.db.execute(
            select(func.count())
            .select_from(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.role == role
            )
        )
        return result.scalar() or 0
