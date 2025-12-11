"""
SIMBA Backend - Base LLM Client

Abstract base class for LLM integrations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, AsyncGenerator, Optional
from app.models.message import Message


class BaseLLMClient(ABC):
    """Base class for LLM clients"""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Send chat completion request (non-streaming).

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """
        Send streaming chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional provider-specific parameters

        Yields:
            Token chunks as they arrive
        """
        pass

    @abstractmethod
    async def chat_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Send chat completion with tool calling support.

        Args:
            messages: List of message dicts
            tools: List of tool definitions
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Dict with 'content' and optional 'tool_calls'
        """
        pass

    def format_messages(self, messages: List[Message]) -> List[Dict[str, str]]:
        """
        Format Message objects to provider-specific format.

        Args:
            messages: List of Message objects

        Returns:
            List of formatted message dicts
        """
        formatted = []
        for msg in messages:
            formatted.append({
                "role": msg.role,
                "content": msg.content
            })
        return formatted
