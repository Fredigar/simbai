"""
SIMBA Backend - User Models

Pydantic models for User entity.
"""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# Base User model (shared fields)
class UserBase(BaseModel):
    """Base user fields"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


# User creation request
class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8)


# User update request
class UserUpdate(BaseModel):
    """User update schema"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    settings: Optional[Dict[str, Any]] = None


# User response (what API returns)
class User(UserBase):
    """User response schema"""
    id: str
    created_at: datetime
    settings: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True  # For SQLAlchemy compatibility


# User with API keys (admin only)
class UserWithKeys(User):
    """User with API keys (sensitive data)"""
    api_keys: Dict[str, str] = Field(default_factory=dict)
