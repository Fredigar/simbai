"""
SIMBA Backend - Tool Models

Pydantic models for Tool and ToolProvider entities.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl


# Tool parameter schema
class ToolParameter(BaseModel):
    """Tool parameter definition"""
    type: str  # string, number, boolean, object, array
    description: str
    required: bool = False
    default: Optional[Any] = None
    enum: Optional[List[Any]] = None


# Base Tool model
class ToolBase(BaseModel):
    """Base tool fields"""
    name: str = Field(..., pattern=r'^[a-zA-Z0-9_]+$')  # Function name format
    description: str
    enabled: bool = True
    icon: Optional[str] = None
    category: Optional[str] = None


# Tool creation
class ToolCreate(ToolBase):
    """Tool creation schema"""
    provider_id: str
    parameters: Dict[str, ToolParameter] = Field(default_factory=dict)


# Tool update
class ToolUpdate(BaseModel):
    """Tool update schema"""
    description: Optional[str] = None
    enabled: Optional[bool] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    parameters: Optional[Dict[str, ToolParameter]] = None


# Tool response
class Tool(ToolBase):
    """Tool response schema"""
    id: str
    provider_id: str
    parameters: Dict[str, ToolParameter] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Tool for LLM (OpenAI function calling format)
class ToolForLLM(BaseModel):
    """Tool formatted for LLM API"""
    type: Literal["function"] = "function"
    function: Dict[str, Any]  # name, description, parameters


# Provider configuration
class ProviderConfig(BaseModel):
    """Provider configuration"""
    url: Optional[HttpUrl] = None
    auth_type: Optional[Literal["basic", "bearer", "api_key", "oauth"]] = None
    timeout: int = Field(default=30, ge=1, le=300)
    max_retries: int = Field(default=3, ge=0, le=10)
    additional_config: Dict[str, Any] = Field(default_factory=dict)


# Base ToolProvider model
class ToolProviderBase(BaseModel):
    """Base tool provider fields"""
    name: str
    type: str  # confluence, folder, jira, custom, etc.
    enabled: bool = True


# ToolProvider creation
class ToolProviderCreate(ToolProviderBase):
    """ToolProvider creation schema"""
    config: ProviderConfig


# ToolProvider update
class ToolProviderUpdate(BaseModel):
    """ToolProvider update schema"""
    name: Optional[str] = None
    enabled: Optional[bool] = None
    config: Optional[ProviderConfig] = None


# ToolProvider response
class ToolProvider(ToolProviderBase):
    """ToolProvider response schema"""
    id: str
    config: ProviderConfig
    health_status: Literal["healthy", "degraded", "down", "unknown"] = "unknown"
    last_health_check: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ToolProvider with tools
class ToolProviderWithTools(ToolProvider):
    """ToolProvider with its tools"""
    tools: List[Tool] = Field(default_factory=list)


# Health check result
class HealthCheckResult(BaseModel):
    """Provider health check result"""
    provider_id: str
    status: Literal["healthy", "degraded", "down"]
    latency_ms: float
    message: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
