"""
SIMBA Backend - Anthropic Client

Anthropic (Claude) API integration for chat completions.
"""

from typing import List, Dict, Any, AsyncGenerator, Optional
from anthropic import AsyncAnthropic
from app.services.llm.base import BaseLLMClient
from app.utils.logger import logger


class AnthropicClient(BaseLLMClient):
    """Anthropic (Claude) API client"""

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        super().__init__(api_key, model)
        self.client = AsyncAnthropic(api_key=api_key)

    def _format_messages(self, messages: List[Dict[str, str]]) -> tuple[str, List[Dict[str, str]]]:
        """
        Format messages for Anthropic API.
        Anthropic requires system message separate from messages array.

        Args:
            messages: List of message dicts

        Returns:
            Tuple of (system_prompt, formatted_messages)
        """
        system_prompt = ""
        formatted = []

        for msg in messages:
            if msg["role"] == "system":
                system_prompt = msg["content"]
            else:
                formatted.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        return system_prompt, formatted

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
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional Anthropic parameters

        Returns:
            Generated text response
        """
        try:
            logger.info(f"Anthropic chat request: model={self.model}, messages={len(messages)}")

            system_prompt, formatted_messages = self._format_messages(messages)

            response = await self.client.messages.create(
                model=self.model,
                messages=formatted_messages,
                system=system_prompt if system_prompt else None,
                temperature=temperature,
                max_tokens=max_tokens or 4096,
                **kwargs
            )

            content = response.content[0].text
            logger.info(f"Anthropic response: {len(content)} chars")
            return content

        except Exception as e:
            logger.error(f"Anthropic chat error: {e}")
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
            logger.info(f"Anthropic stream request: model={self.model}, messages={len(messages)}")

            system_prompt, formatted_messages = self._format_messages(messages)

            async with self.client.messages.stream(
                model=self.model,
                messages=formatted_messages,
                system=system_prompt if system_prompt else None,
                temperature=temperature,
                max_tokens=max_tokens or 4096,
                **kwargs
            ) as stream:
                async for text in stream.text_stream:
                    yield text

        except Exception as e:
            logger.error(f"Anthropic stream error: {e}")
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
            tools: List of tool definitions in Anthropic format
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Dict with 'content' and optional 'tool_calls'
        """
        try:
            logger.info(f"Anthropic tools request: model={self.model}, tools={len(tools)}")

            system_prompt, formatted_messages = self._format_messages(messages)

            response = await self.client.messages.create(
                model=self.model,
                messages=formatted_messages,
                system=system_prompt if system_prompt else None,
                tools=tools,
                temperature=temperature,
                max_tokens=kwargs.get('max_tokens', 4096),
                **{k: v for k, v in kwargs.items() if k != 'max_tokens'}
            )

            result = {
                "content": "",
                "tool_calls": []
            }

            # Process response content
            for block in response.content:
                if block.type == "text":
                    result["content"] += block.text
                elif block.type == "tool_use":
                    result["tool_calls"].append({
                        "id": block.id,
                        "name": block.name,
                        "arguments": block.input
                    })

            logger.info(f"Anthropic tools response: {len(result['tool_calls'])} calls")
            return result

        except Exception as e:
            logger.error(f"Anthropic tools error: {e}")
            raise
