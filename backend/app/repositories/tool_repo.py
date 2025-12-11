"""
SIMBA Backend - Tool Repository

Repository for Tool and ToolProvider models with custom queries.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Tool, ToolProvider
from app.repositories.base import BaseRepository


class ToolRepository(BaseRepository[Tool]):
    """Repository for Tool operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(Tool, db)

    async def get_by_name(self, name: str) -> Optional[Tool]:
        """Get tool by name"""
        result = await self.db.execute(
            select(Tool).where(Tool.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_provider(self, provider_id: str) -> List[Tool]:
        """Get all tools for a provider"""
        result = await self.db.execute(
            select(Tool)
            .where(Tool.provider_id == provider_id)
            .order_by(Tool.name)
        )
        return list(result.scalars().all())

    async def get_enabled(self) -> List[Tool]:
        """Get all enabled tools"""
        result = await self.db.execute(
            select(Tool)
            .where(Tool.enabled == True)
            .order_by(Tool.name)
        )
        return list(result.scalars().all())

    async def get_by_category(self, category: str) -> List[Tool]:
        """Get tools by category"""
        result = await self.db.execute(
            select(Tool)
            .where(Tool.category == category)
            .order_by(Tool.name)
        )
        return list(result.scalars().all())


class ToolProviderRepository(BaseRepository[ToolProvider]):
    """Repository for ToolProvider operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(ToolProvider, db)

    async def get_by_name(self, name: str) -> Optional[ToolProvider]:
        """Get provider by name"""
        result = await self.db.execute(
            select(ToolProvider).where(ToolProvider.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_type(self, provider_type: str) -> List[ToolProvider]:
        """Get providers by type"""
        result = await self.db.execute(
            select(ToolProvider)
            .where(ToolProvider.type == provider_type)
            .order_by(ToolProvider.name)
        )
        return list(result.scalars().all())

    async def get_enabled(self) -> List[ToolProvider]:
        """Get all enabled providers"""
        result = await self.db.execute(
            select(ToolProvider)
            .where(ToolProvider.enabled == True)
            .order_by(ToolProvider.name)
        )
        return list(result.scalars().all())

    async def get_healthy(self) -> List[ToolProvider]:
        """Get all healthy providers"""
        result = await self.db.execute(
            select(ToolProvider)
            .where(
                ToolProvider.enabled == True,
                ToolProvider.health_status == "healthy"
            )
            .order_by(ToolProvider.name)
        )
        return list(result.scalars().all())

    async def update_health_status(
        self,
        provider_id: str,
        status: str,
        last_error: Optional[str] = None
    ) -> Optional[ToolProvider]:
        """Update provider health status"""
        return await self.update(
            provider_id,
            health_status=status,
            last_health_check=None,  # Will be set by timestamp mixin
            last_error=last_error
        )
