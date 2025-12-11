"""
SIMBA Backend - Conversation Repository

Repository for Conversation model with custom queries.
"""

from typing import List, Optional
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Conversation, Message, Assistant
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    """Repository for Conversation operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(Conversation, db)

    async def get_with_assistant(self, id: str) -> Optional[Conversation]:
        """Get conversation with assistant details"""
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.assistant))
            .where(Conversation.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[Conversation]:
        """Get conversations for a user"""
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.assistant))
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_message_count(self, conversation_id: str) -> int:
        """Get count of messages in conversation"""
        result = await self.db.execute(
            select(func.count())
            .select_from(Message)
            .where(Message.conversation_id == conversation_id)
        )
        return result.scalar() or 0

    async def search_by_title(
        self,
        user_id: str,
        query: str,
        limit: int = 20
    ) -> List[Conversation]:
        """Search conversations by title"""
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.assistant))
            .where(
                Conversation.user_id == user_id,
                Conversation.title.ilike(f"%{query}%")
            )
            .order_by(Conversation.updated_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_stats(self, user_id: str) -> dict:
        """Get conversation statistics for user"""
        # Total conversations
        total_convs = await self.count(user_id=user_id)

        # Total messages
        result = await self.db.execute(
            select(func.count())
            .select_from(Message)
            .join(Conversation)
            .where(Conversation.user_id == user_id)
        )
        total_messages = result.scalar() or 0

        # Most used assistant
        result = await self.db.execute(
            select(
                Assistant.name,
                func.count(Conversation.id).label("count")
            )
            .select_from(Conversation)
            .join(Assistant)
            .where(Conversation.user_id == user_id)
            .group_by(Assistant.name)
            .order_by(func.count(Conversation.id).desc())
            .limit(1)
        )
        most_used = result.first()

        return {
            "total_conversations": total_convs,
            "total_messages": total_messages,
            "most_used_assistant": most_used[0] if most_used else None,
        }
