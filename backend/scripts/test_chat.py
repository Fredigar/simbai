"""
SIMBA Backend - Chat Service Test Script

Test chat functionality including:
- Creating conversations
- Sending messages (non-streaming)
- Streaming responses
- Testing with different models
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.services.chat_service import ChatService
from app.repositories import AssistantRepository, UserRepository
from app.utils.logger import logger
from app.config import settings


async def test_chat_service():
    """Test chat service with non-streaming messages"""
    logger.info("=== Testing Chat Service (Non-Streaming) ===\n")

    async with AsyncSessionLocal() as db:
        try:
            # Get services
            chat_service = ChatService(db)
            assistant_repo = AssistantRepository(db)
            user_repo = UserRepository(db)

            # Get test user
            user = await user_repo.get_by_username("testuser")
            if not user:
                logger.error("Test user not found. Run seed_data.py first.")
                return

            # Get SIMBA assistant
            assistant = await assistant_repo.get_by_name("SIMBA Assistant")
            if not assistant:
                logger.error("SIMBA Assistant not found. Run seed_data.py first.")
                return

            logger.info(f"User: {user.username}")
            logger.info(f"Assistant: {assistant.name}\n")

            # Create conversation
            logger.info("Creating conversation...")
            conversation = await chat_service.create_conversation(
                user_id=user.id,
                assistant_id=assistant.id,
                title="Test Chat - Non-Streaming"
            )
            logger.info(f"✓ Created conversation: {conversation.id}\n")

            # Test message 1
            logger.info("Sending message 1...")
            logger.info("User: Hello! Can you tell me what you are?")

            message1 = await chat_service.send_message(
                conversation_id=conversation.id,
                content="Hello! Can you tell me what you are?",
                user_id=user.id
            )

            logger.info(f"Assistant: {message1.content}\n")

            # Test message 2
            logger.info("Sending message 2...")
            logger.info("User: What can you help me with?")

            message2 = await chat_service.send_message(
                conversation_id=conversation.id,
                content="What can you help me with?",
                user_id=user.id
            )

            logger.info(f"Assistant: {message2.content}\n")

            # Get all messages
            logger.info("Getting conversation history...")
            messages = await chat_service.get_conversation_messages(conversation.id)
            logger.info(f"✓ Conversation has {len(messages)} messages total\n")

            logger.info("✓ Chat service test completed successfully!")

        except Exception as e:
            logger.error(f"✗ Chat service test failed: {e}")
            import traceback
            traceback.print_exc()


async def test_streaming_chat():
    """Test chat service with streaming responses"""
    logger.info("\n\n=== Testing Chat Service (Streaming) ===\n")

    async with AsyncSessionLocal() as db:
        try:
            # Get services
            chat_service = ChatService(db)
            assistant_repo = AssistantRepository(db)
            user_repo = UserRepository(db)

            # Get test user and assistant
            user = await user_repo.get_by_username("testuser")
            assistant = await assistant_repo.get_by_name("Code Assistant")

            if not user or not assistant:
                logger.error("Test data not found. Run seed_data.py first.")
                return

            logger.info(f"User: {user.username}")
            logger.info(f"Assistant: {assistant.name}\n")

            # Create conversation
            logger.info("Creating conversation...")
            conversation = await chat_service.create_conversation(
                user_id=user.id,
                assistant_id=assistant.id,
                title="Test Chat - Streaming"
            )
            logger.info(f"✓ Created conversation: {conversation.id}\n")

            # Stream message
            logger.info("Streaming message...")
            logger.info("User: Write a simple Python function to calculate factorial")
            logger.info("Assistant: ", end="", flush=True)

            full_response = ""
            async for chunk in chat_service.stream_message(
                conversation_id=conversation.id,
                content="Write a simple Python function to calculate factorial",
                user_id=user.id
            ):
                if chunk.type == "token":
                    print(chunk.content, end="", flush=True)
                    full_response += chunk.content
                elif chunk.type == "done":
                    logger.info(f"\n\n✓ Message saved with ID: {chunk.message_id}")
                elif chunk.type == "error":
                    logger.error(f"\n✗ Error: {chunk.error}")

            logger.info("\n✓ Streaming test completed successfully!")

        except Exception as e:
            logger.error(f"\n✗ Streaming test failed: {e}")
            import traceback
            traceback.print_exc()


async def test_different_models():
    """Test different LLM models"""
    logger.info("\n\n=== Testing Different Models ===\n")

    # Check which API keys are configured
    has_openai = bool(settings.OPENAI_API_KEY)
    has_anthropic = bool(settings.ANTHROPIC_API_KEY)

    logger.info("API Keys Configuration:")
    logger.info(f"  OpenAI: {'✓ Configured' if has_openai else '✗ Not configured'}")
    logger.info(f"  Anthropic: {'✓ Configured' if has_anthropic else '✗ Not configured'}\n")

    if not has_openai and not has_anthropic:
        logger.warning("No API keys configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in .env")
        logger.info("Example .env file:")
        logger.info("OPENAI_API_KEY=sk-...")
        logger.info("ANTHROPIC_API_KEY=sk-ant-...")
        return

    async with AsyncSessionLocal() as db:
        try:
            chat_service = ChatService(db)
            user_repo = UserRepository(db)

            user = await user_repo.get_by_username("testuser")
            if not user:
                logger.error("Test user not found.")
                return

            # Test available models
            if has_openai:
                logger.info("Testing OpenAI GPT-4...")
                from app.services.llm import OpenAIClient

                client = OpenAIClient(
                    api_key=settings.OPENAI_API_KEY,
                    model="gpt-4"
                )

                response = await client.chat(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Say 'Hello from GPT-4!' in one sentence."}
                    ],
                    temperature=0.7,
                    max_tokens=50
                )

                logger.info(f"✓ GPT-4 Response: {response}\n")

            if has_anthropic:
                logger.info("Testing Anthropic Claude...")
                from app.services.llm import AnthropicClient

                client = AnthropicClient(
                    api_key=settings.ANTHROPIC_API_KEY,
                    model="claude-3-5-sonnet-20241022"
                )

                response = await client.chat(
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": "Say 'Hello from Claude!' in one sentence."}
                    ],
                    temperature=0.7
                )

                logger.info(f"✓ Claude Response: {response}\n")

            logger.info("✓ Model tests completed!")

        except Exception as e:
            logger.error(f"✗ Model test failed: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Run all tests"""
    logger.info("=" * 70)
    logger.info("SIMBA Chat Service Tests")
    logger.info("=" * 70)

    # Check API keys first
    has_keys = bool(settings.OPENAI_API_KEY) or bool(settings.ANTHROPIC_API_KEY)

    if not has_keys:
        logger.warning("\n⚠ No API keys configured!")
        logger.info("\nTo test chat functionality, you need to configure at least one LLM provider:")
        logger.info("\n1. Create a .env file in the backend directory:")
        logger.info("   cd /home/user/simbai/backend")
        logger.info("   touch .env")
        logger.info("\n2. Add your API key(s):")
        logger.info("   OPENAI_API_KEY=sk-...")
        logger.info("   # or")
        logger.info("   ANTHROPIC_API_KEY=sk-ant-...")
        logger.info("\n3. Run this test again\n")
        return

    # Run tests
    await test_different_models()

    # Only run full tests if keys are available
    if has_keys:
        await test_chat_service()
        await test_streaming_chat()

    logger.info("\n" + "=" * 70)
    logger.info("All tests completed!")
    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
