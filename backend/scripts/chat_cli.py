"""
SIMBA Backend - Interactive Chat CLI

Simple interactive chat interface for testing.
Works with or without API keys (uses mock when no keys available).
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict, Any, AsyncGenerator, Optional

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.services.chat_service import ChatService
from app.services.llm.base import BaseLLMClient
from app.repositories import AssistantRepository, UserRepository
from app.config import settings
from app.utils.logger import logger


class MockLLMClient(BaseLLMClient):
    """Mock LLM for demo when no API keys"""

    RESPONSES = [
        "¡Hola! Soy un asistente mock para demostración. Para usar LLMs reales, configura OPENAI_API_KEY o ANTHROPIC_API_KEY en el archivo .env",
        "Interesante pregunta. En un escenario real, consultaría mi modelo de lenguaje para darte una respuesta detallada.",
        "Eso suena fascinante. Con acceso a un LLM real, podría ayudarte mejor con eso.",
        "Entiendo. En modo demo, mis respuestas son limitadas, pero la infraestructura está lista para LLMs reales.",
        "¡Buena observación! El sistema está completamente funcional, solo necesita una API key para conectarse a OpenAI o Anthropic.",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(api_key="mock", model="mock")
        self.response_index = 0

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        # Rotate through responses
        response = self.RESPONSES[self.response_index % len(self.RESPONSES)]
        self.response_index += 1
        await asyncio.sleep(0.5)  # Simulate thinking
        return response

    async def stream_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> AsyncGenerator[str, None]:
        response = self.RESPONSES[self.response_index % len(self.RESPONSES)]
        self.response_index += 1

        # Stream word by word
        words = response.split()
        for i, word in enumerate(words):
            if i > 0:
                yield " "
            yield word
            await asyncio.sleep(0.05)

    async def chat_with_tools(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        return {
            "content": await self.chat(messages, temperature, **kwargs),
            "tool_calls": []
        }


def print_banner():
    """Print welcome banner"""
    print("\n" + "=" * 70)
    print("  SIMBA - Sistema Inteligente de Mensajería con Backend Avanzado")
    print("  Interactive Chat CLI")
    print("=" * 70)


def print_instructions():
    """Print usage instructions"""
    print("\nInstrucciones:")
    print("  • Escribe tus mensajes y presiona Enter")
    print("  • Escribe 'exit' o 'quit' para salir")
    print("  • Escribe 'help' para ver comandos")
    print("  • Escribe 'clear' para limpiar el historial")
    print()


def print_help():
    """Print help message"""
    print("\nComandos disponibles:")
    print("  help     - Mostrar esta ayuda")
    print("  exit     - Salir del chat")
    print("  quit     - Salir del chat")
    print("  clear    - Limpiar historial de conversación")
    print("  status   - Ver estado de la conversación")
    print()


async def select_assistant(db):
    """Let user select an assistant"""
    assistant_repo = AssistantRepository(db)
    assistants = await assistant_repo.get_multi(limit=10)

    print("\nAsistentes disponibles:")
    for i, assistant in enumerate(assistants, 1):
        print(f"  {i}. {assistant.name}")
        print(f"     {assistant.greeting}")
        print()

    while True:
        try:
            choice = input("Selecciona un asistente (1-{}): ".format(len(assistants)))
            idx = int(choice) - 1
            if 0 <= idx < len(assistants):
                return assistants[idx]
            else:
                print("❌ Número inválido. Intenta de nuevo.")
        except ValueError:
            print("❌ Por favor ingresa un número.")
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            sys.exit(0)


async def chat_loop(conversation_id: str, assistant_name: str, user_id: str, use_mock: bool):
    """Main chat loop"""
    message_count = 0

    # Patch ChatService to use mock if needed
    if use_mock:
        original_get_client = ChatService._get_llm_client

        def mock_get_client(self, model, api_key=None):
            return MockLLMClient()

        ChatService._get_llm_client = mock_get_client

    print(f"\n💬 Chateando con {assistant_name}")
    print("=" * 70)

    if use_mock:
        print("\n⚠️  MODO DEMO: Usando respuestas simuladas")
        print("   Para usar LLMs reales, configura API keys en .env\n")
    else:
        print(f"\n✓ Conectado con LLM real ({settings.OPENAI_API_KEY and 'OpenAI' or 'Anthropic'})\n")

    while True:
        try:
            # Get user input
            user_input = input("\n🧑 Tú: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.lower() in ['exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break

            if user_input.lower() == 'help':
                print_help()
                continue

            if user_input.lower() == 'clear':
                print("\n" * 50)  # Clear screen
                print(f"💬 Chateando con {assistant_name}")
                print("=" * 70)
                print("\n✓ Historial limpiado (visualmente)\n")
                continue

            if user_input.lower() == 'status':
                print(f"\n📊 Estado:")
                print(f"   Conversación ID: {conversation_id}")
                print(f"   Mensajes enviados: {message_count}")
                print(f"   Modo: {'DEMO (Mock)' if use_mock else 'REAL (LLM)'}")
                continue

            # Send message
            print(f"\n🤖 {assistant_name}: ", end="", flush=True)

            async with AsyncSessionLocal() as db:
                chat_service = ChatService(db)

                # Stream response
                full_response = ""
                async for chunk in chat_service.stream_message(
                    conversation_id=conversation_id,
                    content=user_input,
                    user_id=user_id
                ):
                    if chunk.type == "token":
                        print(chunk.content, end="", flush=True)
                        full_response += chunk.content
                    elif chunk.type == "error":
                        print(f"\n\n❌ Error: {chunk.error}")
                        break

                print()  # New line after response
                message_count += 1

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            print("Intenta de nuevo o escribe 'exit' para salir.")


async def main():
    """Main function"""
    print_banner()

    # Check API keys
    has_keys = bool(settings.OPENAI_API_KEY) or bool(settings.ANTHROPIC_API_KEY)
    use_mock = not has_keys

    if use_mock:
        print("\n⚠️  No se detectaron API keys")
        print("   Modo: DEMO (respuestas simuladas)")
        print("\n   Para usar LLMs reales:")
        print("   1. Crea un archivo .env en /home/user/simbai/backend/")
        print("   2. Agrega: OPENAI_API_KEY=sk-... o ANTHROPIC_API_KEY=sk-ant-...")
        print("   3. Ejecuta este script de nuevo")
    else:
        api_provider = "OpenAI" if settings.OPENAI_API_KEY else "Anthropic"
        print(f"\n✓ API Key detectada: {api_provider}")
        print("   Modo: REAL (LLM conectado)")

    print_instructions()

    try:
        async with AsyncSessionLocal() as db:
            # Get user
            user_repo = UserRepository(db)
            user = await user_repo.get_by_username("testuser")

            if not user:
                print("❌ Usuario de prueba no encontrado.")
                print("   Ejecuta: python scripts/seed_data.py")
                return

            # Select assistant
            assistant = await select_assistant(db)
            print(f"\n✓ Asistente seleccionado: {assistant.name}")

            # Create conversation
            chat_service = ChatService(db)
            conversation = await chat_service.create_conversation(
                user_id=user.id,
                assistant_id=assistant.id,
                title=f"Chat CLI - {assistant.name}"
            )

            # Ensure conversation is committed to database
            await db.commit()

            print(f"✓ Conversación creada: {conversation.id}")

        # Start chat loop
        await chat_loop(
            conversation_id=conversation.id,
            assistant_name=assistant.name,
            user_id=user.id,
            use_mock=use_mock
        )

        # Show final stats
        async with AsyncSessionLocal() as db:
            chat_service = ChatService(db)
            messages = await chat_service.get_conversation_messages(conversation.id)
            print(f"\n📊 Estadísticas finales:")
            print(f"   Total de mensajes: {len(messages)}")
            print(f"   Conversación ID: {conversation.id}")

    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
    except Exception as e:
        print(f"\n\n❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
