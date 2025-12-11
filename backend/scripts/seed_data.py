"""
SIMBA Backend - Seed Data Script

Populate database with initial assistants and test data.
"""

import asyncio
import uuid
from datetime import datetime

from sqlalchemy import select

# Add parent directory to path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.db.models import Assistant, User
from app.utils.logger import logger


async def seed_assistants():
    """Seed initial assistants"""
    assistants_data = [
        {
            "id": str(uuid.uuid4()),
            "name": "SIMBA Assistant",
            "avatar_url": "/assets/avatars/simba.png",
            "main_image_url": "/assets/images/simba-main.jpg",
            "greeting": "Hello! I'm SIMBA, your intelligent assistant. How can I help you today?",
            "placeholder": "Ask me anything...",
            "model": "gpt-4",
            "temperature": 0.7,
            "system_prompt": "You are SIMBA, a helpful and intelligent assistant with access to various tools and knowledge bases.",
            "tools": [],
            "quick_actions": [
                {
                    "id": "summarize",
                    "label": "Summarize",
                    "icon": "doc_text",
                    "prompt": "Please summarize the key points from our conversation."
                },
                {
                    "id": "explain",
                    "label": "Explain",
                    "icon": "lightbulb",
                    "prompt": "Please explain this concept in simple terms."
                }
            ],
            "device_selector": False,
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Code Assistant",
            "avatar_url": "/assets/avatars/code-assistant.png",
            "main_image_url": "/assets/images/code-main.jpg",
            "greeting": "Hi! I'm your Code Assistant. I can help with programming, debugging, and technical questions.",
            "placeholder": "Describe your coding problem...",
            "model": "gpt-4",
            "temperature": 0.3,
            "system_prompt": "You are an expert programming assistant. Help users with code, debugging, architecture decisions, and best practices.",
            "tools": [],
            "quick_actions": [
                {
                    "id": "debug",
                    "label": "Debug",
                    "icon": "bug_report",
                    "prompt": "Help me debug this code."
                },
                {
                    "id": "optimize",
                    "label": "Optimize",
                    "icon": "speed",
                    "prompt": "How can I optimize this code?"
                },
                {
                    "id": "review",
                    "label": "Review",
                    "icon": "fact_check",
                    "prompt": "Please review this code for best practices."
                }
            ],
            "device_selector": False,
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Research Assistant",
            "avatar_url": "/assets/avatars/research.png",
            "main_image_url": "/assets/images/research-main.jpg",
            "greeting": "Hello! I'm your Research Assistant. I can help you find information and analyze documents.",
            "placeholder": "What would you like to research?",
            "model": "gpt-4",
            "temperature": 0.5,
            "system_prompt": "You are a research assistant. Help users find information, analyze documents, and provide well-sourced answers.",
            "tools": [],
            "quick_actions": [
                {
                    "id": "search",
                    "label": "Search",
                    "icon": "search",
                    "prompt": "Search for information about..."
                },
                {
                    "id": "analyze",
                    "label": "Analyze",
                    "icon": "analytics",
                    "prompt": "Analyze this document."
                }
            ],
            "device_selector": False,
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Creative Assistant",
            "avatar_url": "/assets/avatars/creative.png",
            "main_image_url": "/assets/images/creative-main.jpg",
            "greeting": "Hey! I'm your Creative Assistant. Let's create something amazing together!",
            "placeholder": "What shall we create today?",
            "model": "gpt-4",
            "temperature": 0.9,
            "system_prompt": "You are a creative assistant. Help users with writing, brainstorming, and creative projects.",
            "tools": [],
            "quick_actions": [
                {
                    "id": "brainstorm",
                    "label": "Brainstorm",
                    "icon": "lightbulb",
                    "prompt": "Help me brainstorm ideas for..."
                },
                {
                    "id": "write",
                    "label": "Write",
                    "icon": "edit",
                    "prompt": "Help me write..."
                }
            ],
            "device_selector": False,
        }
    ]

    async with AsyncSessionLocal() as db:
        try:
            # Check if assistants already exist
            result = await db.execute(select(Assistant))
            existing = result.scalars().all()

            if existing:
                logger.info(f"Database already has {len(existing)} assistants. Skipping seed.")
                return

            # Create assistants
            for assistant_data in assistants_data:
                assistant = Assistant(**assistant_data)
                db.add(assistant)
                logger.info(f"Creating assistant: {assistant_data['name']}")

            await db.commit()
            logger.info(f"Successfully seeded {len(assistants_data)} assistants")

        except Exception as e:
            logger.error(f"Error seeding assistants: {e}")
            await db.rollback()
            raise


async def seed_test_user():
    """Seed a test user for development"""
    async with AsyncSessionLocal() as db:
        try:
            # Check if user already exists
            result = await db.execute(select(User).where(User.username == "testuser"))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                logger.info("Test user already exists. Skipping.")
                return

            # Create test user
            test_user = User(
                id=str(uuid.uuid4()),
                username="testuser",
                email="test@example.com",
                hashed_password="$2b$12$dummy_hashed_password",  # Dummy password
                settings={
                    "theme": "dark",
                    "language": "en",
                    "notifications": True
                },
                api_keys={}
            )

            db.add(test_user)
            await db.commit()
            logger.info(f"Created test user: {test_user.username}")

        except Exception as e:
            logger.error(f"Error seeding test user: {e}")
            await db.rollback()
            raise


async def main():
    """Run all seed functions"""
    logger.info("Starting database seeding...")

    try:
        await seed_assistants()
        await seed_test_user()
        logger.info("Database seeding completed successfully!")
    except Exception as e:
        logger.error(f"Database seeding failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
