"""
SIMBA Backend - Chat Service Mock Test

Test chat infrastructure without requiring real API keys.
Uses a mock LLM client for testing.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any, AsyncGenerator, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.services.llm.base import BaseLLMClient
from app.services.chat_service import ChatService
from app.repositories import AssistantRepository, UserRepository
from app.utils.logger import logger


class MockLLMClient(BaseLLMClient):
    """Mock LLM client for testing"""

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """Return mock response"""
        last_message = messages[-1]["content"] if messages else ""
        return f"Mock response to: {last_message}"

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Yield mock streaming response"""
        response = f"Mock streaming response to: {messages[-1]['content']}"
        for word in response.split():
            yield word + " "
            await asyncio.sleep(0.05)  # Simulate delay

    async def chat_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """Return mock response with no tool calls"""
        return {
            "content": f"Mock tool response to: {messages[-1]['content']}",
            "tool_calls": []
        }


async def test_chat_infrastructure():
    """Test chat infrastructure without real LLM calls"""
    logger.info("=== Testing Chat Infrastructure (Mock) ===\n")

    async with AsyncSessionLocal() as db:
        try:
            # Get repositories
            assistant_repo = AssistantRepository(db)
            user_repo = UserRepository(db)

            # Get test data
            user = await user_repo.get_by_username("testuser")
            assistant = await assistant_repo.get_by_name("SIMBA Assistant")

            if not user or not assistant:
                logger.error("Test data not found. Run seed_data.py first.")
                return False

            logger.info(f"✓ Found user: {user.username}")
            logger.info(f"✓ Found assistant: {assistant.name}\n")

            # Test ChatService initialization
            chat_service = ChatService(db)
            logger.info("✓ ChatService initialized\n")

            # Test conversation creation
            logger.info("Testing conversation creation...")
            conversation = await chat_service.create_conversation(
                user_id=user.id,
                assistant_id=assistant.id,
                title="Test Mock Conversation"
            )
            logger.info(f"✓ Created conversation: {conversation.id}\n")

            # Test context building
            logger.info("Testing context building...")
            context = await chat_service._build_context(conversation.id)
            logger.info(f"✓ Built context with {len(context)} messages")
            logger.info(f"  System prompt: {context[0]['content'][:50]}...\n")

            # Test getting messages
            logger.info("Testing message retrieval...")
            messages = await chat_service.get_conversation_messages(conversation.id)
            logger.info(f"✓ Retrieved {len(messages)} messages\n")

            # Test mock LLM client
            logger.info("Testing mock LLM client...")
            mock_client = MockLLMClient(api_key="mock", model="mock-gpt-4")

            test_messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, how are you?"}
            ]

            response = await mock_client.chat(test_messages)
            logger.info(f"✓ Mock response: {response}\n")

            # Test mock streaming
            logger.info("Testing mock streaming...")
            logger.info("Stream: ", end="", flush=True)

            async for chunk in mock_client.stream_chat(test_messages):
                print(chunk, end="", flush=True)

            logger.info("\n✓ Mock streaming completed\n")

            logger.info("✓ All infrastructure tests passed!")
            return True

        except Exception as e:
            logger.error(f"✗ Infrastructure test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def test_database_relationships():
    """Test database relationships for chat"""
    logger.info("\n\n=== Testing Database Relationships ===\n")

    async with AsyncSessionLocal() as db:
        try:
            chat_service = ChatService(db)
            user_repo = UserRepository(db)

            # Get user
            user = await user_repo.get_by_username("testuser")
            assistant_repo = AssistantRepository(db)

            # Get all assistants
            assistants = await assistant_repo.get_multi(limit=10)
            logger.info(f"✓ Found {len(assistants)} assistants")

            for assistant in assistants:
                logger.info(f"  - {assistant.name} ({assistant.model})")

            logger.info()

            # Create conversations with different assistants
            logger.info("Creating test conversations...")
            conversations = []

            for i, assistant in enumerate(assistants[:2]):  # Test with first 2
                conv = await chat_service.create_conversation(
                    user_id=user.id,
                    assistant_id=assistant.id,
                    title=f"Test Conversation {i+1}"
                )
                conversations.append(conv)
                logger.info(f"✓ Created conversation with {assistant.name}")

            logger.info()

            # Get user's conversations
            from app.repositories import ConversationRepository
            conv_repo = ConversationRepository(db)

            user_conversations = await conv_repo.get_by_user(user.id)
            logger.info(f"✓ User has {len(user_conversations)} total conversations")

            # Get conversation stats
            stats = await conv_repo.get_stats(user.id)
            logger.info(f"✓ User stats:")
            logger.info(f"  Total conversations: {stats['total_conversations']}")
            logger.info(f"  Total messages: {stats['total_messages']}")
            logger.info(f"  Most used assistant: {stats.get('most_used_assistant', 'N/A')}")

            logger.info("\n✓ Database relationship tests passed!")
            return True

        except Exception as e:
            logger.error(f"✗ Database relationship test failed: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Run all mock tests"""
    logger.info("=" * 70)
    logger.info("SIMBA Chat Service Mock Tests")
    logger.info("(Testing infrastructure without API keys)")
    logger.info("=" * 70)
    logger.info()

    # Run tests
    test1_passed = await test_chat_infrastructure()
    test2_passed = await test_database_relationships()

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("Test Summary:")
    logger.info(f"  Infrastructure Test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    logger.info(f"  Database Test:       {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    logger.info("=" * 70)

    if test1_passed and test2_passed:
        logger.info("\n✓ All mock tests passed successfully!")
        logger.info("\nTo test with real LLM providers:")
        logger.info("1. Add API keys to .env file")
        logger.info("2. Run: python scripts/test_chat.py")
    else:
        logger.error("\n✗ Some tests failed. Check logs above.")

    return test1_passed and test2_passed


if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)
