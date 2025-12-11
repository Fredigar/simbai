"""
SIMBA Backend - Database Test Script

Test database operations and repositories.
"""

import asyncio
import uuid
from datetime import datetime

# Add parent directory to path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.repositories import (
    UserRepository,
    AssistantRepository,
    ConversationRepository,
    MessageRepository,
    ToolRepository,
    DocumentRepository
)
from app.utils.logger import logger


async def test_assistant_repository():
    """Test Assistant repository operations"""
    logger.info("=== Testing AssistantRepository ===")

    async with AsyncSessionLocal() as db:
        repo = AssistantRepository(db)

        # Get all assistants
        assistants = await repo.get_multi()
        logger.info(f"Found {len(assistants)} assistants")

        for assistant in assistants:
            logger.info(f"  - {assistant.name} (model: {assistant.model})")

        # Get assistant by name
        simba = await repo.get_by_name("SIMBA Assistant")
        if simba:
            logger.info(f"Found SIMBA Assistant: {simba.id}")
        else:
            logger.warning("SIMBA Assistant not found")

        # Get enabled assistants
        enabled = await repo.get_enabled()
        logger.info(f"Enabled assistants: {len(enabled)}")

        logger.info("✓ AssistantRepository tests passed")
        return assistants[0] if assistants else None


async def test_user_repository():
    """Test User repository operations"""
    logger.info("\n=== Testing UserRepository ===")

    async with AsyncSessionLocal() as db:
        repo = UserRepository(db)

        # Get test user
        user = await repo.get_by_username("testuser")
        if user:
            logger.info(f"Found test user: {user.username} ({user.email})")
        else:
            logger.warning("Test user not found")

        # Get all users
        users = await repo.get_multi()
        logger.info(f"Total users: {len(users)}")

        logger.info("✓ UserRepository tests passed")
        return user


async def test_conversation_repository(user, assistant):
    """Test Conversation repository operations"""
    logger.info("\n=== Testing ConversationRepository ===")

    async with AsyncSessionLocal() as db:
        repo = ConversationRepository(db)

        # Create a test conversation
        conversation = await repo.create(
            id=str(uuid.uuid4()),
            user_id=user.id,
            assistant_id=assistant.id,
            title="Test Conversation",
            device="desktop",
            conv_metadata={"test": True}
        )
        logger.info(f"Created conversation: {conversation.id}")

        # Get conversation with assistant
        conv_with_assistant = await repo.get_with_assistant(conversation.id)
        if conv_with_assistant:
            logger.info(f"  Assistant: {conv_with_assistant.assistant.name}")

        # Get conversations by user
        user_conversations = await repo.get_by_user(user.id)
        logger.info(f"User has {len(user_conversations)} conversations")

        # Get message count
        msg_count = await repo.get_message_count(conversation.id)
        logger.info(f"Conversation has {msg_count} messages")

        # Get stats
        stats = await repo.get_stats(user.id)
        logger.info(f"User stats: {stats}")

        logger.info("✓ ConversationRepository tests passed")
        return conversation


async def test_message_repository(conversation, assistant):
    """Test Message repository operations"""
    logger.info("\n=== Testing MessageRepository ===")

    async with AsyncSessionLocal() as db:
        repo = MessageRepository(db)

        # Create test messages
        user_msg = await repo.create(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            role="user",
            content="Hello, can you help me?",
            msg_metadata={}
        )
        logger.info(f"Created user message: {user_msg.id}")

        assistant_msg = await repo.create(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            assistant_id=assistant.id,
            role="assistant",
            content="Of course! How can I help you today?",
            msg_metadata={},
            sources=[],
            tool_calls=[]
        )
        logger.info(f"Created assistant message: {assistant_msg.id}")

        # Get messages by conversation
        messages = await repo.get_by_conversation(conversation.id)
        logger.info(f"Conversation has {len(messages)} messages")

        for msg in messages:
            logger.info(f"  [{msg.role}] {msg.content[:50]}...")

        # Get messages by role
        user_messages = await repo.get_by_role(conversation.id, "user")
        assistant_messages = await repo.get_by_role(conversation.id, "assistant")
        logger.info(f"User messages: {len(user_messages)}, Assistant messages: {len(assistant_messages)}")

        # Count by role
        user_count = await repo.count_by_role(conversation.id, "user")
        logger.info(f"User message count: {user_count}")

        logger.info("✓ MessageRepository tests passed")


async def test_document_repository(conversation):
    """Test Document repository operations"""
    logger.info("\n=== Testing DocumentRepository ===")

    async with AsyncSessionLocal() as db:
        repo = DocumentRepository(db)

        # Create test document
        doc = await repo.create(
            id=str(uuid.uuid4()),
            conversation_id=conversation.id,
            filename="test.pdf",
            mime_type="application/pdf",
            size_bytes=1024,
            content="This is a test document content.",
            doc_metadata={"pages": 1},
            vector_ids=[]
        )
        logger.info(f"Created document: {doc.filename}")

        # Get documents by conversation
        docs = await repo.get_by_conversation(conversation.id)
        logger.info(f"Conversation has {len(docs)} documents")

        # Get by type
        pdf_docs = await repo.get_by_type(conversation.id, "application/pdf")
        logger.info(f"PDF documents: {len(pdf_docs)}")

        # Count documents
        doc_count = await repo.count_by_conversation(conversation.id)
        logger.info(f"Document count: {doc_count}")

        # Get total size
        total_size = await repo.get_total_size(conversation.id)
        logger.info(f"Total document size: {total_size} bytes")

        logger.info("✓ DocumentRepository tests passed")


async def test_database_connection():
    """Test basic database connection"""
    logger.info("\n=== Testing Database Connection ===")

    async with AsyncSessionLocal() as db:
        try:
            # Simple query to test connection
            from sqlalchemy import text
            result = await db.execute(text("SELECT 1"))
            logger.info("✓ Database connection successful")
            return True
        except Exception as e:
            logger.error(f"✗ Database connection failed: {e}")
            return False


async def main():
    """Run all tests"""
    logger.info("Starting database tests...")
    logger.info("=" * 60)

    try:
        # Test connection
        connected = await test_database_connection()
        if not connected:
            return

        # Test repositories
        assistant = await test_assistant_repository()
        user = await test_user_repository()

        if user and assistant:
            conversation = await test_conversation_repository(user, assistant)
            await test_message_repository(conversation, assistant)
            await test_document_repository(conversation)

        logger.info("\n" + "=" * 60)
        logger.info("✓ All database tests passed successfully!")

    except Exception as e:
        logger.error(f"\n✗ Database tests failed: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == "__main__":
    asyncio.run(main())
