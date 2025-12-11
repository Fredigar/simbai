"""
SIMBA Backend - SQLAlchemy ORM Models

Database models using SQLAlchemy ORM.
"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime,
    Text, JSON, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.db.base import Base, TimestampMixin, TableNameMixin


class User(Base, TimestampMixin, TableNameMixin):
    """User ORM model"""

    id = Column(String(36), primary_key=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    settings = Column(JSON, default=dict)
    api_keys = Column(JSON, default=dict)  # Encrypted

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")


class Assistant(Base, TimestampMixin, TableNameMixin):
    """Assistant ORM model"""

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500))
    main_image_url = Column(String(500))
    greeting = Column(Text, default="Hello! How can I help you today?")
    placeholder = Column(String(200), default="Ask me anything...")
    model = Column(String(100), default="gpt-4")
    temperature = Column(Float, default=0.7)
    system_prompt = Column(Text, default="You are a helpful assistant.")
    tools = Column(JSON, default=list)  # List of tool IDs
    quick_actions = Column(JSON, default=list)  # List of quick action configs
    device_selector = Column(Boolean, default=False)

    # Relationships
    conversations = relationship("Conversation", back_populates="assistant")
    messages = relationship("Message", back_populates="assistant")


class Conversation(Base, TimestampMixin, TableNameMixin):
    """Conversation ORM model"""

    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    assistant_id = Column(String(36), ForeignKey("assistants.id"), nullable=False, index=True)
    title = Column(String(200))
    device = Column(String(100))
    conv_metadata = Column(JSON, default=dict)  # Renamed from 'metadata' to avoid SQLAlchemy conflict

    # Relationships
    user = relationship("User", back_populates="conversations")
    assistant = relationship("Assistant", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="conversation", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_conversation_user_updated', 'user_id', 'updated_at'),
    )


class Message(Base, TimestampMixin, TableNameMixin):
    """Message ORM model"""

    id = Column(String(36), primary_key=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False, index=True)
    assistant_id = Column(String(36), ForeignKey("assistants.id"), index=True)
    role = Column(String(20), nullable=False)  # user, assistant, system, tool
    content = Column(Text, nullable=False)
    msg_metadata = Column(JSON, default=dict)  # Renamed from 'metadata' to avoid SQLAlchemy conflict

    # RAG data (stored as JSON)
    sources = Column(JSON, default=list)
    references = Column(JSON, default=list)

    # Tools data
    tool_calls = Column(JSON, default=list)
    tool_results = Column(JSON, default=list)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    assistant = relationship("Assistant", back_populates="messages")

    # Indexes
    __table_args__ = (
        Index('idx_message_conversation_created', 'conversation_id', 'created_at'),
    )


class ToolProvider(Base, TimestampMixin, TableNameMixin):
    """ToolProvider ORM model"""

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)  # confluence, folder, jira, etc.
    enabled = Column(Boolean, default=True)
    config = Column(JSON, nullable=False)  # Provider configuration
    health_status = Column(String(20), default="unknown")
    last_health_check = Column(DateTime)

    # Relationships
    tools = relationship("Tool", back_populates="provider", cascade="all, delete-orphan")


class Tool(Base, TimestampMixin, TableNameMixin):
    """Tool ORM model"""

    id = Column(String(36), primary_key=True)
    provider_id = Column(String(36), ForeignKey("tool_providers.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    parameters = Column(JSON, default=dict)  # Parameter schema
    enabled = Column(Boolean, default=True)
    icon = Column(String(50))
    category = Column(String(50))

    # Relationships
    provider = relationship("ToolProvider", back_populates="tools")

    # Indexes
    __table_args__ = (
        Index('idx_tool_name_enabled', 'name', 'enabled'),
    )


class Document(Base, TimestampMixin, TableNameMixin):
    """Document ORM model"""

    id = Column(String(36), primary_key=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    content = Column(Text)  # Extracted text content
    doc_metadata = Column(JSON, default=dict)  # Renamed from 'metadata' to avoid SQLAlchemy conflict
    vector_ids = Column(JSON, default=list)  # ChromaDB vector IDs
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    conversation = relationship("Conversation", back_populates="documents")

    # Indexes
    __table_args__ = (
        Index('idx_document_conversation', 'conversation_id'),
    )
