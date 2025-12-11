"""
SIMBA Backend - Message Models

Pydantic models for Message entity.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field


# Source model (RAG reference)
class Source(BaseModel):
    """RAG source/reference"""
    id: str
    title: str
    url: Optional[str] = None
    content: str  # Excerpt
    score: float = Field(ge=0.0, le=1.0)  # Relevance score
    provider: str  # confluence, folder, etc.
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Reference model (numbered reference in message)
class Reference(BaseModel):
    """Numbered reference in message"""
    number: int
    source_id: str
    text: str  # Referenced text snippet


# Tool Call model
class ToolCall(BaseModel):
    """Tool call from LLM"""
    id: str
    tool_name: str
    parameters: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Tool Result model
class ToolResult(BaseModel):
    """Result from tool execution"""
    tool_call_id: str
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# Base Message model
class MessageBase(BaseModel):
    """Base message fields"""
    role: Literal["user", "assistant", "system", "tool"]
    content: str


# Message creation
class MessageCreate(MessageBase):
    """Message creation schema"""
    conversation_id: str
    assistant_id: Optional[str] = None  # For assistant messages


# Message update (rarely used)
class MessageUpdate(BaseModel):
    """Message update schema"""
    content: Optional[str] = None
    msg_metadata: Optional[Dict[str, Any]] = None


# Message response
class Message(MessageBase):
    """Message response schema"""
    id: str
    conversation_id: str
    assistant_id: Optional[str] = None
    created_at: datetime
    msg_metadata: Dict[str, Any] = Field(default_factory=dict)

    # RAG data
    sources: List[Source] = Field(default_factory=list)
    references: List[Reference] = Field(default_factory=list)

    # Tools data
    tool_calls: List[ToolCall] = Field(default_factory=list)
    tool_results: List[ToolResult] = Field(default_factory=list)

    class Config:
        from_attributes = True


# Message with assistant info
class MessageWithAssistant(Message):
    """Message with assistant details"""
    assistant_name: Optional[str] = None
    assistant_avatar: Optional[str] = None


# Streaming chunk
class StreamingChunk(BaseModel):
    """Streaming message chunk"""
    type: Literal["token", "sources", "tool_call", "tool_result", "done", "error"]
    content: Optional[str] = None  # For tokens
    sources: Optional[List[Source]] = None
    tool_call: Optional[ToolCall] = None
    tool_result: Optional[ToolResult] = None
    message_id: Optional[str] = None  # For done event
    error: Optional[str] = None  # For error event
