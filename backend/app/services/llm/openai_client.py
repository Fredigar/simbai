"""
SIMBA Backend - OpenAI Client

OpenAI API integration for chat completions.
"""

from typing import List, Dict, Any, AsyncGenerator, Optional
from openai import AsyncOpenAI
from app.services.llm.base import BaseLLMClient
from app.utils.logger import logger


class OpenAIClient(BaseLLMClient):
    """OpenAI API client"""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        super().__init__(api_key, model)
        self.client = AsyncOpenAI(api_key=api_key)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Send non-streaming chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional OpenAI parameters

        Returns:
            Generated text response
        """
        try:
            logger.info(f"OpenAI chat request: model={self.model}, messages={len(messages)}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            content = response.choices[0].message.content
            logger.info(f"OpenAI response: {len(content)} chars")
            return content

        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            raise

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
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Yields:
            Token chunks as they arrive
        """
        try:
            logger.info(f"OpenAI stream request: model={self.model}, messages={len(messages)}")

            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            raise

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
            tools: List of tool definitions in OpenAI format
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Dict with 'content' and optional 'tool_calls'
        """
        try:
            logger.info(f"OpenAI tools request: model={self.model}, tools={len(tools)}")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                temperature=temperature,
                **kwargs
            )

            message = response.choices[0].message
            result = {
                "content": message.content or "",
                "tool_calls": []
            }

            if message.tool_calls:
                result["tool_calls"] = [
                    {
                        "id": tc.id,
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                    for tc in message.tool_calls
                ]

            logger.info(f"OpenAI tools response: {len(result['tool_calls'])} calls")
            return result

        except Exception as e:
            logger.error(f"OpenAI tools error: {e}")
            raise
