"""
SIMBA Backend - Base Repository

Base repository with common CRUD operations.
"""

from typing import Generic, TypeVar, Type, Optional, List, Dict, Any
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository with CRUD operations.

    All repositories inherit from this class.
    """

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        Initialize repository.

        Args:
            model: SQLAlchemy model class
            db: Async database session
        """
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> ModelType:
        """
        Create a new record.

        Args:
            **kwargs: Field values

        Returns:
            Created model instance
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def get(self, id: str) -> Optional[ModelType]:
        """
        Get record by ID.

        Args:
            id: Record ID

        Returns:
            Model instance or None
        """
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: Optional[str] = None,
        **filters
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records
            order_by: Field to order by
            **filters: Filter conditions

        Returns:
            List of model instances
        """
        query = select(self.model)

        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        # Apply ordering
        if order_by and hasattr(self.model, order_by):
            query = query.order_by(getattr(self.model, order_by).desc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def update(self, id: str, **kwargs) -> Optional[ModelType]:
        """
        Update a record.

        Args:
            id: Record ID
            **kwargs: Fields to update

        Returns:
            Updated model instance or None
        """
        # Remove None values
        update_data = {k: v for k, v in kwargs.items() if v is not None}

        if not update_data:
            return await self.get(id)

        await self.db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**update_data)
        )

        await self.db.flush()
        return await self.get(id)

    async def delete(self, id: str) -> bool:
        """
        Delete a record.

        Args:
            id: Record ID

        Returns:
            True if deleted, False if not found
        """
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )

        await self.db.flush()
        return result.rowcount > 0

    async def count(self, **filters) -> int:
        """
        Count records.

        Args:
            **filters: Filter conditions

        Returns:
            Number of records
        """
        from sqlalchemy import func

        query = select(func.count()).select_from(self.model)

        # Apply filters
        for key, value in filters.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = await self.db.execute(query)
        return result.scalar() or 0

    async def exists(self, id: str) -> bool:
        """
        Check if record exists.

        Args:
            id: Record ID

        Returns:
            True if exists, False otherwise
        """
        result = await self.db.execute(
            select(self.model.id).where(self.model.id == id)
        )
        return result.scalar_one_or_none() is not None
