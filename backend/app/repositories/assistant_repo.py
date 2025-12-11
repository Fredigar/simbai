"""
SIMBA Backend - Assistant Repository

Repository for Assistant model with custom queries.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Assistant
from app.repositories.base import BaseRepository


class AssistantRepository(BaseRepository[Assistant]):
    """Repository for Assistant operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(Assistant, db)

    async def get_by_name(self, name: str) -> Optional[Assistant]:
        """Get assistant by name"""
        result = await self.db.execute(
            select(Assistant).where(Assistant.name == name)
        )
        return result.scalar_one_or_none()

    async def get_enabled(self) -> List[Assistant]:
        """Get all enabled assistants (no explicit enabled field, so get all)"""
        result = await self.db.execute(
            select(Assistant).order_by(Assistant.name)
        )
        return list(result.scalars().all())

    async def get_by_model(self, model: str) -> List[Assistant]:
        """Get assistants using specific model"""
        result = await self.db.execute(
            select(Assistant)
            .where(Assistant.model == model)
            .order_by(Assistant.name)
        )
        return list(result.scalars().all())

    async def update_tools(self, assistant_id: str, tool_ids: List[str]) -> Optional[Assistant]:
        """Update assistant's tools"""
        return await self.update(assistant_id, tools=tool_ids)

    async def update_quick_actions(
        self,
        assistant_id: str,
        quick_actions: List[dict]
    ) -> Optional[Assistant]:
        """Update assistant's quick actions"""
        return await self.update(assistant_id, quick_actions=quick_actions)
