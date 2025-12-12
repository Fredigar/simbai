"""
SIMBA Backend - Chat Service

Core chat service orchestrating LLM interactions, message management, and conversation flow.
"""

import uuid
from typing import List, AsyncGenerator, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.llm import OpenAIClient, AnthropicClient, BaseLLMClient
from app.repositories import ConversationRepository, MessageRepository, AssistantRepository
from app.models.message import Message, MessageCreate, StreamingChunk, Source
from app.models.conversation import Conversation
from app.config import settings
from app.utils.logger import logger
from app.utils.exceptions import ChatException


class ChatService:
    """Chat service for managing conversations and LLM interactions"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversation_repo = ConversationRepository(db)
        self.message_repo = MessageRepository(db)
        self.assistant_repo = AssistantRepository(db)

    def _get_llm_client(self, model: str, api_key: Optional[str] = None) -> BaseLLMClient:
        """
        Get appropriate LLM client based on model name.

        Args:
            model: Model identifier (e.g., 'gpt-4', 'claude-3-5-sonnet')
            api_key: Optional API key override

        Returns:
            LLM client instance

        Raises:
            ChatException: If model is unsupported or API key missing
        """
        # Determine provider from model name
        if model.startswith("gpt") or model.startswith("o1"):
            # OpenAI models
            key = api_key or settings.OPENAI_API_KEY
            if not key:
                raise ChatException("OpenAI API key not configured")
            return OpenAIClient(api_key=key, model=model)

        elif model.startswith("claude"):
            # Anthropic models
            key = api_key or settings.ANTHROPIC_API_KEY
            if not key:
                raise ChatException("Anthropic API key not configured")
            return AnthropicClient(api_key=key, model=model)

        else:
            raise ChatException(f"Unsupported model: {model}")

    async def _build_context(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Dict[str, str]]:
        """
        Build conversation context from message history.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages to include

        Returns:
            List of formatted messages for LLM
        """
        # Get conversation
        conversation = await self.conversation_repo.get_with_assistant(conversation_id)
        if not conversation:
            raise ChatException(f"Conversation {conversation_id} not found")

        # Get messages
        messages = await self.message_repo.get_by_conversation(conversation_id, limit=limit)

        # Build context
        context = []

        # Add system prompt
        if conversation.assistant.system_prompt:
            context.append({
                "role": "system",
                "content": conversation.assistant.system_prompt
            })

        # Add message history
        for msg in messages:
            context.append({
                "role": msg.role,
                "content": msg.content
            })

        return context

    async def send_message(
        self,
        conversation_id: str,
        content: str,
        user_id: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Message:
        """
        Send a message and get response (non-streaming).

        Args:
            conversation_id: Conversation ID
            content: User message content
            user_id: User ID sending the message
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Returns:
            Assistant's response message

        Raises:
            ChatException: If conversation not found or LLM error
        """
        try:
            # Get conversation and assistant
            conversation = await self.conversation_repo.get_with_assistant(conversation_id)
            if not conversation:
                raise ChatException(f"Conversation {conversation_id} not found")

            assistant = conversation.assistant

            # Create user message
            user_msg = await self.message_repo.create(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                role="user",
                content=content,
                msg_metadata={}
            )

            logger.info(f"Created user message: {user_msg.id}")

            # Build context
            context = await self._build_context(conversation_id)

            # Get LLM client
            llm = self._get_llm_client(assistant.model)

            # Call LLM
            response_content = await llm.chat(
                messages=context,
                temperature=temperature or assistant.temperature,
                max_tokens=max_tokens
            )

            # Create assistant message
            assistant_msg = await self.message_repo.create(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                assistant_id=assistant.id,
                role="assistant",
                content=response_content,
                msg_metadata={},
                sources=[],
                tool_calls=[]
            )

            # Update conversation timestamp
            await self.conversation_repo.update(conversation_id, updated_at=datetime.utcnow())

            logger.info(f"Created assistant message: {assistant_msg.id}")

            # Convert ORM to Pydantic
            return Message.model_validate(assistant_msg)

        except Exception as e:
            logger.error(f"Send message error: {e}")
            raise ChatException(f"Failed to send message: {str(e)}")

    async def stream_message(
        self,
        conversation_id: str,
        content: str,
        user_id: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> AsyncGenerator[StreamingChunk, None]:
        """
        Send a message and stream the response.

        Args:
            conversation_id: Conversation ID
            content: User message content
            user_id: User ID sending the message
            temperature: Optional temperature override
            max_tokens: Optional max tokens override

        Yields:
            StreamingChunk objects with incremental response

        Raises:
            ChatException: If conversation not found or LLM error
        """
        try:
            # Get conversation and assistant
            conversation = await self.conversation_repo.get_with_assistant(conversation_id)
            if not conversation:
                raise ChatException(f"Conversation {conversation_id} not found")

            assistant = conversation.assistant

            # Create user message
            user_msg = await self.message_repo.create(
                id=str(uuid.uuid4()),
                conversation_id=conversation_id,
                role="user",
                content=content,
                msg_metadata={}
            )

            logger.info(f"Created user message: {user_msg.id}")

            # Build context
            context = await self._build_context(conversation_id)

            # Get LLM client
            llm = self._get_llm_client(assistant.model)

            # Stream response
            full_response = ""
            message_id = str(uuid.uuid4())

            async for token in llm.stream_chat(
                messages=context,
                temperature=temperature or assistant.temperature,
                max_tokens=max_tokens
            ):
                full_response += token
                yield StreamingChunk(
                    type="token",
                    content=token
                )

            # Create assistant message with full response
            assistant_msg = await self.message_repo.create(
                id=message_id,
                conversation_id=conversation_id,
                assistant_id=assistant.id,
                role="assistant",
                content=full_response,
                msg_metadata={},
                sources=[],
                tool_calls=[]
            )

            # Update conversation timestamp
            await self.conversation_repo.update(conversation_id, updated_at=datetime.utcnow())

            logger.info(f"Created assistant message: {assistant_msg.id}")

            # Send done event
            yield StreamingChunk(
                type="done",
                message_id=message_id
            )

        except Exception as e:
            logger.error(f"Stream message error: {e}")
            yield StreamingChunk(
                type="error",
                error=str(e)
            )

    async def create_conversation(
        self,
        user_id: str,
        assistant_id: str,
        title: Optional[str] = None,
        device: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation.

        Args:
            user_id: User ID
            assistant_id: Assistant ID
            title: Optional conversation title
            device: Optional device identifier

        Returns:
            Created conversation

        Raises:
            ChatException: If assistant not found
        """
        try:
            # Verify assistant exists
            assistant = await self.assistant_repo.get(assistant_id)
            if not assistant:
                raise ChatException(f"Assistant {assistant_id} not found")

            # Create conversation
            conversation = await self.conversation_repo.create(
                id=str(uuid.uuid4()),
                user_id=user_id,
                assistant_id=assistant_id,
                title=title or f"Conversation with {assistant.name}",
                device=device,
                conv_metadata={}
            )

            logger.info(f"Created conversation: {conversation.id}")

            return Conversation.model_validate(conversation)

        except Exception as e:
            logger.error(f"Create conversation error: {e}")
            raise ChatException(f"Failed to create conversation: {str(e)}")

    async def get_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Message]:
        """
        Get messages from a conversation.

        Args:
            conversation_id: Conversation ID
            limit: Maximum number of messages
            offset: Offset for pagination

        Returns:
            List of messages
        """
        messages = await self.message_repo.get_by_conversation(
            conversation_id,
            skip=offset,
            limit=limit
        )

        return [Message.model_validate(msg) for msg in messages]
