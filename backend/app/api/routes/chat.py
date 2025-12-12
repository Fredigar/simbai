"""
SIMBA Backend - Chat API Routes

Chat endpoints for sending messages and managing conversations.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.chat_service import ChatService
from app.models.message import Message
from app.models.conversation import Conversation
from app.utils.logger import logger
from app.utils.exceptions import ChatException


router = APIRouter(prefix="/chat", tags=["chat"])


# Request/Response models
class SendMessageRequest(BaseModel):
    """Request to send a message"""
    conversation_id: str
    content: str = Field(..., min_length=1, max_length=10000)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, ge=1, le=16000)


class CreateConversationRequest(BaseModel):
    """Request to create a conversation"""
    assistant_id: str
    title: Optional[str] = Field(None, max_length=200)
    device: Optional[str] = None


class MessageResponse(BaseModel):
    """Message response"""
    message: Message
    conversation_id: str


@router.post("/send", response_model=MessageResponse)
async def send_message(
    request: SendMessageRequest,
    user_id: str = "testuser",  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message and get response (non-streaming).

    Args:
        request: Message request
        user_id: User ID (from auth)
        db: Database session

    Returns:
        Assistant's response message
    """
    try:
        chat_service = ChatService(db)

        message = await chat_service.send_message(
            conversation_id=request.conversation_id,
            content=request.content,
            user_id=user_id,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )

        return MessageResponse(
            message=message,
            conversation_id=request.conversation_id
        )

    except ChatException as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post("/stream")
async def stream_message(
    request: SendMessageRequest,
    user_id: str = "testuser",  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Send a message and stream the response.

    Args:
        request: Message request
        user_id: User ID (from auth)
        db: Database session

    Returns:
        Streaming response with Server-Sent Events
    """
    async def event_generator():
        """Generate SSE events"""
        try:
            chat_service = ChatService(db)

            async for chunk in chat_service.stream_message(
                conversation_id=request.conversation_id,
                content=request.content,
                user_id=user_id,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            ):
                # Format as SSE
                data = chunk.model_dump_json()
                yield f"data: {data}\n\n"

        except ChatException as e:
            logger.error(f"Stream error: {e}")
            error_chunk = {
                "type": "error",
                "error": str(e)
            }
            yield f"data: {error_chunk}\n\n"
        except Exception as e:
            logger.error(f"Unexpected stream error: {e}")
            error_chunk = {
                "type": "error",
                "error": "Internal server error"
            }
            yield f"data: {error_chunk}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@router.post("/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    request: CreateConversationRequest,
    user_id: str = "testuser",  # TODO: Get from auth
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new conversation.

    Args:
        request: Conversation creation request
        user_id: User ID (from auth)
        db: Database session

    Returns:
        Created conversation
    """
    try:
        chat_service = ChatService(db)

        conversation = await chat_service.create_conversation(
            user_id=user_id,
            assistant_id=request.assistant_id,
            title=request.title,
            device=request.device
        )

        return conversation

    except ChatException as e:
        logger.error(f"Create conversation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(
    conversation_id: str,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get messages from a conversation.

    Args:
        conversation_id: Conversation ID
        limit: Maximum number of messages
        offset: Offset for pagination
        db: Database session

    Returns:
        List of messages
    """
    try:
        chat_service = ChatService(db)

        messages = await chat_service.get_conversation_messages(
            conversation_id=conversation_id,
            limit=limit,
            offset=offset
        )

        return messages

    except Exception as e:
        logger.error(f"Get messages error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
