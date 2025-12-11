"""
SIMBA Backend - Database Base

SQLAlchemy base and common utilities.
"""

from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models"""
    pass


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


class TableNameMixin:
    """Mixin to auto-generate table names"""

    @declared_attr
    def __tablename__(cls):
        # Convert CamelCase to snake_case and pluralize
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        # Simple pluralization (add 's')
        if not name.endswith('s'):
            name += 's'
        return name
