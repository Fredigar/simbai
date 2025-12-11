"""
SIMBA Backend - Document Repository

Repository for Document model with custom queries.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document
from app.repositories.base import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """Repository for Document operations"""

    def __init__(self, db: AsyncSession):
        super().__init__(Document, db)

    async def get_by_conversation(
        self,
        conversation_id: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[Document]:
        """Get documents for a conversation"""
        result = await self.db.execute(
            select(Document)
            .where(Document.conversation_id == conversation_id)
            .order_by(Document.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_by_type(
        self,
        conversation_id: str,
        mime_type: str
    ) -> List[Document]:
        """Get documents by MIME type"""
        result = await self.db.execute(
            select(Document)
            .where(
                Document.conversation_id == conversation_id,
                Document.mime_type == mime_type
            )
            .order_by(Document.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_filename(
        self,
        conversation_id: str,
        filename: str
    ) -> Optional[Document]:
        """Get document by filename in conversation"""
        result = await self.db.execute(
            select(Document)
            .where(
                Document.conversation_id == conversation_id,
                Document.filename == filename
            )
        )
        return result.scalar_one_or_none()

    async def count_by_conversation(self, conversation_id: str) -> int:
        """Count documents in conversation"""
        from sqlalchemy import func

        result = await self.db.execute(
            select(func.count())
            .select_from(Document)
            .where(Document.conversation_id == conversation_id)
        )
        return result.scalar() or 0

    async def get_total_size(self, conversation_id: str) -> int:
        """Get total file size for conversation documents"""
        from sqlalchemy import func

        result = await self.db.execute(
            select(func.sum(Document.size_bytes))
            .where(Document.conversation_id == conversation_id)
        )
        return result.scalar() or 0

    async def search_by_content(
        self,
        conversation_id: str,
        search_term: str,
        limit: int = 20
    ) -> List[Document]:
        """Search documents by content"""
        result = await self.db.execute(
            select(Document)
            .where(
                Document.conversation_id == conversation_id,
                Document.content.ilike(f"%{search_term}%")
            )
            .order_by(Document.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
