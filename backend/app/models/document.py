"""
SIMBA Backend - Document Models

Pydantic models for Document entity (uploaded files).
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# Base Document model
class DocumentBase(BaseModel):
    """Base document fields"""
    filename: str
    mime_type: str


# Document creation
class DocumentCreate(DocumentBase):
    """Document creation schema"""
    conversation_id: str
    content: str  # Extracted text
    size_bytes: int
    doc_metadata: Dict[str, Any] = Field(default_factory=dict)


# Document update
class DocumentUpdate(BaseModel):
    """Document update schema"""
    doc_metadata: Optional[Dict[str, Any]] = None


# Document response
class Document(DocumentBase):
    """Document response schema"""
    id: str
    conversation_id: str
    size_bytes: int
    content: str  # Extracted text
    doc_metadata: Dict[str, Any] = Field(default_factory=dict)
    vector_ids: List[str] = Field(default_factory=list)  # ChromaDB IDs
    uploaded_at: datetime

    class Config:
        from_attributes = True


# Document list item (without content)
class DocumentListItem(BaseModel):
    """Document minimal info for list"""
    id: str
    filename: str
    mime_type: str
    size_bytes: int
    uploaded_at: datetime
    indexed: bool = False  # Has vector embeddings

    class Config:
        from_attributes = True


# Document upload response
class DocumentUploadResponse(BaseModel):
    """Response after uploading document"""
    document_id: str
    filename: str
    size_bytes: int
    indexed: bool
    extraction_status: str  # success, partial, failed


# Document processing status
class DocumentProcessingStatus(BaseModel):
    """Document processing status"""
    document_id: str
    status: str  # pending, processing, completed, failed
    progress: float = Field(ge=0.0, le=1.0)
    message: Optional[str] = None
