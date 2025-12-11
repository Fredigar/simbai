"""
SIMBA Backend - Conversation Models

Pydantic models for Conversation entity.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


# Base Conversation model
class ConversationBase(BaseModel):
    """Base conversation fields"""
    title: Optional[str] = Field(None, max_length=200)
    device: Optional[str] = None


# Conversation creation
class ConversationCreate(ConversationBase):
    """Conversation creation schema"""
    assistant_id: str
    user_id: str


# Conversation update
class ConversationUpdate(BaseModel):
    """Conversation update schema"""
    title: Optional[str] = Field(None, max_length=200)
    device: Optional[str] = None
    conv_metadata: Optional[Dict[str, Any]] = None


# Conversation response
class Conversation(ConversationBase):
    """Conversation response schema"""
    id: str
    user_id: str
    assistant_id: str
    created_at: datetime
    updated_at: datetime
    conv_metadata: Dict[str, Any] = Field(default_factory=dict)
    message_count: int = 0  # Computed field

    class Config:
        from_attributes = True


# Conversation with assistant info
class ConversationWithAssistant(Conversation):
    """Conversation with assistant details"""
    assistant_name: str
    assistant_avatar: Optional[str] = None


# Conversation list item
class ConversationListItem(BaseModel):
    """Conversation minimal info for list"""
    id: str
    title: Optional[str]
    assistant_id: str
    assistant_name: str
    updated_at: datetime
    message_count: int

    class Config:
        from_attributes = True


# Conversation statistics
class ConversationStats(BaseModel):
    """Conversation statistics"""
    total_conversations: int
    total_messages: int
    most_used_assistant: Optional[str] = None
    total_tokens: int = 0
