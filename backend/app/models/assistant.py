"""
SIMBA Backend - Assistant Models

Pydantic models for Assistant entity.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


# Quick Action model
class QuickAction(BaseModel):
    """Quick action button configuration"""
    id: str
    label: str
    prompt: str
    icon: Optional[str] = None
    is_selection: bool = False  # Requires text selection


# Base Assistant model
class AssistantBase(BaseModel):
    """Base assistant fields"""
    name: str = Field(..., min_length=1, max_length=100)
    avatar_url: Optional[HttpUrl] = None
    main_image_url: Optional[HttpUrl] = None
    greeting: str = Field(default="Hello! How can I help you today?")
    placeholder: str = Field(default="Ask me anything...")
    model: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    system_prompt: str = Field(default="You are a helpful assistant.")
    device_selector: bool = Field(default=False)


# Assistant creation
class AssistantCreate(AssistantBase):
    """Assistant creation schema"""
    tools: List[str] = Field(default_factory=list)  # Tool IDs
    quick_actions: List[QuickAction] = Field(default_factory=list)


# Assistant update
class AssistantUpdate(BaseModel):
    """Assistant update schema"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[HttpUrl] = None
    main_image_url: Optional[HttpUrl] = None
    greeting: Optional[str] = None
    placeholder: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    system_prompt: Optional[str] = None
    tools: Optional[List[str]] = None
    quick_actions: Optional[List[QuickAction]] = None
    device_selector: Optional[bool] = None


# Assistant response
class Assistant(AssistantBase):
    """Assistant response schema"""
    id: str
    tools: List[str] = Field(default_factory=list)
    quick_actions: List[QuickAction] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Assistant list item (minimal fields for list view)
class AssistantListItem(BaseModel):
    """Assistant minimal info for list"""
    id: str
    name: str
    avatar_url: Optional[HttpUrl] = None
    greeting: str

    class Config:
        from_attributes = True
