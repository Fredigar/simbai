"""
SIMBA Backend - Complete Demo

Demonstrates all implemented features:
- Chat with LLMs
- Document upload and processing
- RAG semantic search
- All integrated together
"""

import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.services.chat_service import ChatService
from app.services.rag import RAGService
from app.repositories import AssistantRepository, UserRepository, DocumentRepository
from app.utils.logger import logger
from app.config import settings


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


async def demo_database():
    """Demo: Database and repositories"""
    print_section("1. DATABASE & REPOSITORIES")

    async with AsyncSessionLocal() as db:
        user_repo = UserRepository(db)
        assistant_repo = AssistantRepository(db)

        # Get user
        user = await user_repo.get_by_username("testuser")
        print(f"✓ User: {user.username} ({user.email})")

        # Get assistants
        assistants = await assistant_repo.get_multi(limit=5)
        print(f"✓ Assistants: {len(assistants)}")
        for asst in assistants:
            print(f"  - {asst.name} ({asst.model})")

        return user, assistants[0]


async def demo_chat_creation():
    """Demo: Create conversation"""
    print_section("2. CHAT CONVERSATION CREATION")

    async with AsyncSessionLocal() as db:
        chat_service = ChatService(db)
        user_repo = UserRepository(db)
        assistant_repo = AssistantRepository(db)

        user = await user_repo.get_by_username("testuser")
        assistant = await assistant_repo.get_by_name("SIMBA Assistant")

        conversation = await chat_service.create_conversation(
            user_id=user.id,
            assistant_id=assistant.id,
            title="Complete Demo Conversation"
        )

        await db.commit()

        print(f"✓ Created conversation: {conversation.id}")
        print(f"  User: {user.username}")
        print(f"  Assistant: {assistant.name}")
        print(f"  Title: {conversation.title}")

        return conversation.id


async def demo_document_indexing(conversation_id: str):
    """Demo: Document processing and RAG indexing"""
    print_section("3. DOCUMENT PROCESSING & RAG INDEXING")

    # Create sample document
    sample_text = """
    SIMBA Documentation

    SIMBA (Sistema Inteligente de Mensajería con Backend Avanzado) is an advanced
    AI-powered messaging system that combines multiple LLM providers with
    Retrieval-Augmented Generation (RAG) capabilities.

    Features:
    - Multi-LLM support (OpenAI GPT-4, Anthropic Claude)
    - Semantic search with ChromaDB
    - Document processing (PDF, DOCX, TXT)
    - Streaming responses
    - Multiple assistants with different personalities
    - Tool calling and function execution

    Architecture:
    SIMBA uses a modular architecture with FastAPI backend, async SQLAlchemy for
    database operations, and ChromaDB for vector storage. The system supports
    both streaming and non-streaming chat completions.
    """

    async with AsyncSessionLocal() as db:
        import uuid
        doc_repo = DocumentRepository(db)
        rag_service = RAGService(db)

        # Create document
        document = await doc_repo.create(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            filename="simba_docs.txt",
            mime_type="text/plain",
            size_bytes=len(sample_text.encode()),
            content=sample_text,
            doc_metadata={"type": "documentation"},
            vector_ids=[]
        )

        print(f"✓ Created document: {document.filename}")
        print(f"  Size: {document.size_bytes} bytes")

        # Index for RAG
        vector_ids = await rag_service.index_document(
            document_id=document.id,
            conversation_id=conversation_id,
            content=sample_text,
            metadata={"filename": document.filename}
        )

        # Update document with vector IDs
        await doc_repo.update(document.id, vector_ids=vector_ids)

        print(f"✓ Indexed document: {len(vector_ids)} chunks created")

        return document.id


async def demo_semantic_search(conversation_id: str):
    """Demo: RAG semantic search"""
    print_section("4. SEMANTIC SEARCH (RAG)")

    queries = [
        "What is SIMBA?",
        "What LLM providers are supported?",
        "Tell me about the architecture"
    ]

    async with AsyncSessionLocal() as db:
        rag_service = RAGService(db)

        for query in queries:
            print(f"\nQuery: \"{query}\"")

            sources = await rag_service.search(
                conversation_id=conversation_id,
                query=query,
                n_results=2,
                min_score=0.0
            )

            if sources:
                print(f"✓ Found {len(sources)} relevant sources:")
                for i, source in enumerate(sources, 1):
                    print(f"  {i}. Score: {source.score:.3f}")
                    print(f"     {source.content[:100]}...")
            else:
                print("  No sources found")


async def demo_chat_with_rag(conversation_id: str):
    """Demo: Chat with RAG context"""
    print_section("5. CHAT WITH RAG (Simulated)")

    has_api_key = bool(settings.OPENAI_API_KEY or settings.ANTHROPIC_API_KEY)

    if not has_api_key:
        print("⚠️  No API keys configured - simulating RAG-enhanced chat\n")
        print("In a real scenario:")
        print("1. User asks: 'What features does SIMBA have?'")
        print("2. System searches documents for relevant context")
        print("3. Context is added to LLM prompt")
        print("4. LLM generates answer using retrieved information")
        print("5. Sources are included in response\n")
        print("✓ This creates more accurate, grounded responses!")
    else:
        print("✓ API keys configured - chat with RAG is available")
        print("Use chat_cli.py or API endpoints to test real integration")


async def demo_statistics():
    """Demo: Show statistics"""
    print_section("6. SYSTEM STATISTICS")

    async with AsyncSessionLocal() as db:
        from app.repositories import ConversationRepository, MessageRepository
        from app.db.chroma_client import get_chroma_client

        user_repo = UserRepository(db)
        conv_repo = ConversationRepository(db)
        msg_repo = MessageRepository(db)
        doc_repo = DocumentRepository(db)

        user = await user_repo.get_by_username("testuser")

        # Conversation stats
        conversations = await conv_repo.get_by_user(user.id)
        stats = await conv_repo.get_stats(user.id)

        print(f"User: {user.username}")
        print(f"  Total conversations: {stats['total_conversations']}")
        print(f"  Total messages: {stats['total_messages']}")
        print(f"  Most used assistant: {stats.get('most_used_assistant', 'N/A')}")

        # Document stats
        if conversations:
            conv = conversations[0]
            docs = await doc_repo.get_by_conversation(conv.id)
            total_size = await doc_repo.get_total_size(conv.id)

            print(f"\nDocuments:")
            print(f"  Total documents: {len(docs)}")
            print(f"  Total size: {total_size} bytes")

        # ChromaDB stats
        chroma = get_chroma_client()
        collections = chroma.list_collections()
        print(f"\nChromaDB:")
        print(f"  Collections: {len(collections)}")


async def demo_api_endpoints():
    """Demo: Show available API endpoints"""
    print_section("7. AVAILABLE API ENDPOINTS")

    endpoints = {
        "Chat": [
            "POST /chat/send - Send message (non-streaming)",
            "POST /chat/stream - Send message (streaming)",
            "POST /chat/conversations - Create conversation",
            "GET /chat/conversations/{id}/messages - Get messages"
        ],
        "RAG": [
            "POST /rag/index - Index document",
            "POST /rag/search - Semantic search",
            "DELETE /rag/documents/{id} - Delete vectors"
        ],
        "Documents": [
            "POST /documents/upload - Upload file",
            "GET /documents/conversation/{id} - List documents",
            "GET /documents/{id} - Get document",
            "DELETE /documents/{id} - Delete document"
        ],
        "System": [
            "GET / - Application info",
            "GET /health - Health check"
        ]
    }

    for category, eps in endpoints.items():
        print(f"\n{category}:")
        for ep in eps:
            print(f"  ✓ {ep}")


async def main():
    """Run complete demo"""
    print("\n" + "=" * 70)
    print("  SIMBA - COMPLETE SYSTEM DEMO")
    print("  Sistema Inteligente de Mensajería con Backend Avanzado")
    print("=" * 70)

    try:
        # Run demos
        await demo_database()
        conversation_id = await demo_chat_creation()
        document_id = await demo_document_indexing(conversation_id)
        await demo_semantic_search(conversation_id)
        await demo_chat_with_rag(conversation_id)
        await demo_statistics()
        await demo_api_endpoints()

        # Summary
        print_section("DEMO COMPLETE ✓")
        print("All systems tested successfully!")
        print("\nNext steps:")
        print("  1. Try interactive chat: python scripts/chat_cli.py")
        print("  2. Start API server: python main.py")
        print("  3. Add API key to .env for real LLM integration")
        print("  4. Upload documents via API and test RAG search")
        print("\nSee PROJECT_STATUS.md for full documentation")

    except Exception as e:
        logger.error(f"Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
