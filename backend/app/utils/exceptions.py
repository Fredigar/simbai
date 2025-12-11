"""
SIMBA Backend - Custom Exceptions

Centralized exception definitions with meaningful error messages.
"""

from typing import Any


class SIMBAException(Exception):
    """Base exception for SIMBA"""

    def __init__(self, message: str, details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


# Chat Exceptions
class ChatException(SIMBAException):
    """Base exception for chat-related errors"""
    pass


class StreamingError(ChatException):
    """Error during message streaming"""
    pass


class MessageProcessingError(ChatException):
    """Error processing message"""
    pass


# RAG Exceptions
class RAGException(SIMBAException):
    """Base exception for RAG-related errors"""
    pass


class EmbeddingError(RAGException):
    """Error generating embeddings"""
    pass


class SearchError(RAGException):
    """Error during semantic search"""
    pass


class IndexingError(RAGException):
    """Error indexing documents"""
    pass


# Tool Exceptions
class ToolException(SIMBAException):
    """Base exception for tool-related errors"""
    pass


class ToolNotFoundError(ToolException):
    """Tool not found in registry"""
    pass


class ToolExecutionError(ToolException):
    """Error executing tool"""
    pass


class ProviderError(ToolException):
    """Error with tool provider"""
    pass


class ProviderNotFoundError(ToolException):
    """Provider not found"""
    pass


# File Exceptions
class FileException(SIMBAException):
    """Base exception for file-related errors"""
    pass


class FileUploadError(FileException):
    """Error uploading file"""
    pass


class FileProcessingError(FileException):
    """Error processing file"""
    pass


class UnsupportedFileTypeError(FileException):
    """Unsupported file type"""
    pass


# Database Exceptions
class DatabaseException(SIMBAException):
    """Base exception for database errors"""
    pass


class RecordNotFoundError(DatabaseException):
    """Database record not found"""
    pass


class DuplicateRecordError(DatabaseException):
    """Duplicate record in database"""
    pass


# LLM Exceptions
class LLMException(SIMBAException):
    """Base exception for LLM-related errors"""
    pass


class LLMAPIError(LLMException):
    """Error calling LLM API"""
    pass


class LLMTimeoutError(LLMException):
    """LLM API timeout"""
    pass


class InvalidLLMResponseError(LLMException):
    """Invalid response from LLM"""
    pass


# Configuration Exceptions
class ConfigurationError(SIMBAException):
    """Configuration error"""
    pass


# Validation Exceptions
class ValidationError(SIMBAException):
    """Validation error"""
    pass


# Authentication/Authorization Exceptions
class AuthenticationError(SIMBAException):
    """Authentication failed"""
    pass


class AuthorizationError(SIMBAException):
    """Authorization failed"""
    pass


# Helper function to create HTTP exception responses
def create_error_response(exc: SIMBAException) -> dict:
    """Create standardized error response"""
    return {
        "error": type(exc).__name__,
        "message": exc.message,
        "details": exc.details,
    }
