# SIMBA - Sistema de Chat Inteligente con IA
## Arquitectura Completa v2.0

**Fecha**: 2024-12-11
**Autor**: Senior Software Architect
**Versión**: 2.0.0 (Complete Rewrite)

---

## 📋 ÍNDICE

1. [Visión General](#1-visión-general)
2. [Principios de Diseño](#2-principios-de-diseño)
3. [Stack Tecnológico](#3-stack-tecnológico)
4. [Arquitectura del Sistema](#4-arquitectura-del-sistema)
5. [Modelo de Datos](#5-modelo-de-datos)
6. [Backend Architecture](#6-backend-architecture)
7. [Frontend Architecture](#7-frontend-architecture)
8. [API Contracts](#8-api-contracts)
9. [Módulos del Sistema](#9-módulos-del-sistema)
10. [Flujos de Datos](#10-flujos-de-datos)
11. [State Management](#11-state-management)
12. [Seguridad](#12-seguridad)
13. [Performance](#13-performance)
14. [Deployment](#14-deployment)

---

## 1. Visión General

### 1.1 ¿Qué es SIMBA?

**SIMBA** (Sistema Inteligente de Mensajería con Backend Avanzado) es una aplicación de chat con IA que integra:

- 🤖 Múltiples asistentes especializados
- 🔍 Sistema RAG (Retrieval-Augmented Generation)
- 🛠️ Herramientas dinámicas extensibles
- 🧠 Reasoning y orquestación multi-paso
- 📊 Visualización de datos avanzada
- 📎 Procesamiento inteligente de archivos
- 🖼️ Análisis de imágenes con Vision AI

### 1.2 Objetivos

- ✅ **Modularidad**: Arquitectura limpia y mantenible
- ✅ **Extensibilidad**: Fácil agregar nuevas herramientas y providers
- ✅ **Performance**: Respuestas rápidas y streaming eficiente
- ✅ **Escalabilidad**: Soportar múltiples usuarios concurrentes
- ✅ **Mantenibilidad**: Código bien documentado y testeable

### 1.3 Usuarios

- **Equipos técnicos**: Consultas sobre documentación interna
- **Analistas**: Análisis de datos y visualización
- **Desarrolladores**: Troubleshooting y code analysis
- **Gestores de conocimiento**: Búsqueda en documentación corporativa

---

## 2. Principios de Diseño

### 2.1 SOLID Principles

✅ **Single Responsibility**: Cada módulo una responsabilidad
✅ **Open/Closed**: Abierto a extensión, cerrado a modificación
✅ **Liskov Substitution**: Providers intercambiables
✅ **Interface Segregation**: APIs específicas y pequeñas
✅ **Dependency Inversion**: Dependencias inyectadas

### 2.2 Separation of Concerns

```
┌─────────────┐
│  Frontend   │ ← UI, UX, State Management
├─────────────┤
│  Backend    │ ← Business Logic, AI, Tools
├─────────────┤
│  Data Layer │ ← Database, ChromaDB, Storage
└─────────────┘
```

### 2.3 Design Patterns

- **Repository Pattern**: Abstracción de persistencia
- **Strategy Pattern**: Providers de herramientas intercambiables
- **Observer Pattern**: State updates y eventos
- **Factory Pattern**: Creación de asistentes y tools
- **Middleware Pattern**: Request/response processing

---

## 3. Stack Tecnológico

### 3.1 Backend

| Componente | Tecnología | Propósito |
|------------|-----------|-----------|
| **Framework** | FastAPI | REST API + WebSockets |
| **Runtime** | Python 3.11+ | Async/await nativo |
| **Vector DB** | ChromaDB | Embeddings y RAG |
| **Database** | SQLite/PostgreSQL | Persistencia relacional |
| **Cache** | Redis (opcional) | Cache de sesiones |
| **AI SDK** | OpenAI SDK, Anthropic SDK | Integración con LLMs |
| **File Processing** | PyMuPDF, python-docx, openpyxl | Extracción de contenido |
| **Vision** | OpenAI Vision, Claude Vision | Análisis de imágenes |

### 3.2 Frontend

| Componente | Tecnología | Propósito |
|------------|-----------|-----------|
| **Framework** | Framework7 | UI Components |
| **Templates** | Lit HTML | Reactive rendering |
| **State** | Custom Store | Centralized state |
| **Charts** | Chart.js | Visualización de datos |
| **Markdown** | Marked.js | Rendering markdown |
| **Syntax Highlight** | Highlight.js | Code blocks |
| **Storage** | IndexedDB | Offline storage |

### 3.3 Infrastructure

- **Container**: Docker + Docker Compose
- **Reverse Proxy**: Nginx
- **Process Manager**: Gunicorn/Uvicorn
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana

---

## 4. Arquitectura del Sistema

### 4.1 Diagrama General

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   Chat   │  │Assistant │  │  Tools   │             │
│  │   UI     │  │  Manager │  │  Panel   │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │              │                     │
│       └─────────────┴──────────────┘                     │
│                     │                                     │
│              ┌──────▼──────┐                            │
│              │ State Store │                            │
│              └──────┬──────┘                            │
│                     │                                     │
└─────────────────────┼─────────────────────────────────┘
                      │ WebSocket + REST
┌─────────────────────┼─────────────────────────────────┐
│                     │         BACKEND                   │
│              ┌──────▼──────┐                            │
│              │  FastAPI    │                            │
│              │  Router     │                            │
│              └──────┬──────┘                            │
│                     │                                     │
│      ┌──────────────┼──────────────┐                    │
│      │              │              │                     │
│  ┌───▼────┐  ┌─────▼─────┐  ┌────▼────┐               │
│  │  Chat  │  │    RAG    │  │  Tools  │               │
│  │Service │  │  Engine   │  │ Manager │               │
│  └───┬────┘  └─────┬─────┘  └────┬────┘               │
│      │              │              │                     │
└──────┼──────────────┼──────────────┼───────────────────┘
       │              │              │
┌──────▼──────────────▼──────────────▼───────────────────┐
│                 DATA LAYER                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ SQLite/  │  │ ChromaDB │  │  Redis   │             │
│  │ Postgres │  │ (Vectors)│  │ (Cache)  │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Flujo de Request

```
1. User types message → Frontend
2. Frontend → WebSocket → Backend
3. Backend → Process message
4. If RAG needed → ChromaDB search
5. If tools needed → Execute tools
6. Backend → LLM API (streaming)
7. Backend → Stream tokens → Frontend
8. Frontend → Render message (live)
9. Frontend → Update state
10. Backend → Save to DB
```

---

## 5. Modelo de Datos

### 5.1 Entidades Core

#### User

```python
class User:
    id: str              # UUID
    username: str
    email: str
    created_at: datetime
    settings: dict       # JSON config
    api_keys: dict       # Encrypted keys
```

#### Assistant

```python
class Assistant:
    id: str              # UUID
    name: str
    avatar_url: str
    main_image_url: str
    greeting: str
    placeholder: str
    model: str           # LLM model to use
    temperature: float
    system_prompt: str
    tools: list[str]     # Tool IDs available
    quick_actions: list[dict]
    device_selector: bool
    created_at: datetime
    updated_at: datetime
```

#### Conversation

```python
class Conversation:
    id: str              # UUID
    user_id: str
    title: str           # Auto-generated or manual
    assistant_id: str    # Main assistant
    device: str | None   # Selected device
    created_at: datetime
    updated_at: datetime
    metadata: dict       # Tags, category, etc.
```

#### Message

```python
class Message:
    id: str              # UUID
    conversation_id: str
    role: str            # 'user', 'assistant', 'system', 'tool'
    content: str         # Message content
    assistant_id: str | None  # If assistant message
    metadata: dict       # Sources, tools_used, tokens, etc.
    created_at: datetime

    # RAG specific
    sources: list[Source]
    references: list[Reference]

    # Tools specific
    tool_calls: list[ToolCall]
    tool_results: list[ToolResult]
```

#### Source (RAG)

```python
class Source:
    id: str
    title: str
    url: str
    content: str         # Excerpt
    score: float         # Relevance score
    provider: str        # confluence, folder, etc.
    metadata: dict       # Page number, section, etc.
```

#### Tool

```python
class Tool:
    id: str
    name: str            # Function name
    description: str
    parameters: dict     # JSON Schema
    provider_id: str     # Which provider
    enabled: bool
    icon: str
    category: str
```

#### ToolProvider

```python
class ToolProvider:
    id: str
    name: str
    type: str            # confluence, folder, jira, custom
    config: dict         # URL, auth, etc.
    enabled: bool
    health_status: str   # healthy, degraded, down
    tools: list[Tool]
```

#### Document

```python
class Document:
    id: str
    conversation_id: str
    filename: str
    mime_type: str
    size_bytes: int
    content: str         # Extracted text
    metadata: dict       # Pages, author, etc.
    vector_ids: list[str]  # ChromaDB IDs
    uploaded_at: datetime
```

### 5.2 Relaciones

```
User (1) ──< (n) Conversation
Conversation (1) ──< (n) Message
Message (1) ──< (n) Source
Message (1) ──< (n) ToolCall
Assistant (1) ──< (n) Message
Assistant (1) ──< (n) Tool
ToolProvider (1) ──< (n) Tool
Conversation (1) ──< (n) Document
```

---

## 6. Backend Architecture

### 6.1 Estructura de Carpetas

```
backend/
├── main.py                    # Entry point
├── requirements.txt
├── Dockerfile
├── .env.example
│
├── app/
│   ├── __init__.py
│   ├── config.py             # Configuration management
│   │
│   ├── api/                  # API layer
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── chat.py       # Chat endpoints
│   │   │   ├── assistants.py
│   │   │   ├── conversations.py
│   │   │   ├── tools.py
│   │   │   ├── documents.py
│   │   │   └── config.py
│   │   │
│   │   └── websockets/
│   │       └── chat.py       # WebSocket handlers
│   │
│   ├── core/                 # Business logic
│   │   ├── __init__.py
│   │   │
│   │   ├── chat/
│   │   │   ├── chat_service.py
│   │   │   ├── streaming.py
│   │   │   └── message_processor.py
│   │   │
│   │   ├── rag/
│   │   │   ├── rag_engine.py
│   │   │   ├── embeddings.py
│   │   │   ├── retrievers.py
│   │   │   └── reranker.py
│   │   │
│   │   ├── reasoning/
│   │   │   ├── orchestrator.py
│   │   │   ├── planner.py
│   │   │   └── executor.py
│   │   │
│   │   ├── tools/
│   │   │   ├── tool_manager.py
│   │   │   ├── tool_registry.py
│   │   │   ├── tool_executor.py
│   │   │   │
│   │   │   └── providers/
│   │   │       ├── base.py
│   │   │       ├── confluence.py
│   │   │       ├── folder.py
│   │   │       ├── jira.py
│   │   │       └── custom.py
│   │   │
│   │   ├── files/
│   │   │   ├── file_processor.py
│   │   │   ├── extractors/
│   │   │   │   ├── pdf.py
│   │   │   │   ├── docx.py
│   │   │   │   ├── xlsx.py
│   │   │   │   └── images.py
│   │   │   └── indexer.py
│   │   │
│   │   └── vision/
│   │       ├── vision_service.py
│   │       └── image_analyzer.py
│   │
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── assistant.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── tool.py
│   │   └── document.py
│   │
│   ├── repositories/         # Data access
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_repo.py
│   │   ├── conversation_repo.py
│   │   ├── message_repo.py
│   │   └── vector_repo.py
│   │
│   ├── services/             # External services
│   │   ├── __init__.py
│   │   ├── llm_service.py    # OpenAI, Anthropic, etc.
│   │   ├── embedding_service.py
│   │   └── storage_service.py
│   │
│   ├── utils/                # Utilities
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── validators.py
│   │   ├── exceptions.py
│   │   └── helpers.py
│   │
│   └── db/                   # Database
│       ├── __init__.py
│       ├── base.py
│       ├── session.py
│       └── migrations/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
└── docs/
    ├── api.md
    └── deployment.md
```

### 6.2 Componentes Backend Clave

#### 6.2.1 Chat Service

```python
class ChatService:
    """
    Orquesta el flujo completo de chat

    Responsibilidades:
    - Recibir mensajes del usuario
    - Activar RAG si es necesario
    - Ejecutar tools si es necesario
    - Llamar al LLM
    - Streamear respuestas
    - Guardar en DB
    """

    def __init__(
        self,
        llm_service: LLMService,
        rag_engine: RAGEngine,
        tool_manager: ToolManager,
        message_repo: MessageRepository
    ):
        self.llm = llm_service
        self.rag = rag_engine
        self.tools = tool_manager
        self.messages = message_repo

    async def process_message(
        self,
        conversation_id: str,
        user_message: str,
        assistant_id: str
    ) -> AsyncGenerator[str, None]:
        """Process user message and stream response"""

        # 1. RAG: Search relevant documents
        sources = await self.rag.search(user_message)

        # 2. Build context
        context = self._build_context(conversation_id, sources)

        # 3. Prepare tools
        available_tools = await self.tools.get_tools_for_assistant(assistant_id)

        # 4. Stream LLM response
        async for chunk in self.llm.stream_chat(
            messages=context,
            tools=available_tools
        ):
            # Handle tool calls if any
            if chunk.tool_calls:
                tool_results = await self.tools.execute_all(chunk.tool_calls)
                # Continue with tool results
                continue

            # Stream text
            yield chunk.content

        # 5. Save message
        await self.messages.create(...)
```

#### 6.2.2 RAG Engine

```python
class RAGEngine:
    """
    Búsqueda semántica y recuperación de documentos

    Responsabilidades:
    - Indexar documentos en ChromaDB
    - Búsqueda por embeddings
    - Re-ranking de resultados
    - Extracción de referencias
    """

    def __init__(
        self,
        chroma_client: ChromaClient,
        embedding_service: EmbeddingService,
        reranker: Reranker
    ):
        self.chroma = chroma_client
        self.embeddings = embedding_service
        self.reranker = reranker

    async def search(
        self,
        query: str,
        top_k: int = 10,
        filters: dict = None
    ) -> list[Source]:
        """Semantic search in documents"""

        # 1. Generate query embedding
        query_embedding = await self.embeddings.embed(query)

        # 2. Search in ChromaDB
        results = self.chroma.query(
            query_embeddings=[query_embedding],
            n_results=top_k * 2,  # Over-fetch for reranking
            where=filters
        )

        # 3. Rerank results
        reranked = await self.reranker.rerank(query, results)

        # 4. Convert to Source objects
        sources = [
            Source(
                id=r['id'],
                title=r['metadata']['title'],
                content=r['document'],
                score=r['score'],
                provider=r['metadata']['provider'],
                url=r['metadata'].get('url'),
                metadata=r['metadata']
            )
            for r in reranked[:top_k]
        ]

        return sources

    async def index_document(
        self,
        document: Document,
        chunk_size: int = 1000
    ):
        """Index document into ChromaDB"""

        # 1. Chunk document
        chunks = self._chunk_text(document.content, chunk_size)

        # 2. Generate embeddings
        embeddings = await self.embeddings.embed_batch(chunks)

        # 3. Store in ChromaDB
        ids = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            doc_id = f"{document.id}_chunk_{i}"
            self.chroma.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[chunk],
                metadatas=[{
                    'document_id': document.id,
                    'chunk_index': i,
                    'title': document.filename,
                    'provider': 'uploaded',
                    **document.metadata
                }]
            )
            ids.append(doc_id)

        return ids
```

#### 6.2.3 Tool Manager

```python
class ToolManager:
    """
    Gestión y ejecución de herramientas dinámicas

    Responsabilidades:
    - Registro de providers
    - Discovery de tools
    - Ejecución de tool calls
    - Health checks
    """

    def __init__(self, tool_repo: ToolRepository):
        self.repo = tool_repo
        self.providers: dict[str, BaseProvider] = {}
        self.registry: dict[str, Tool] = {}

    def register_provider(self, provider: BaseProvider):
        """Register a tool provider"""
        self.providers[provider.id] = provider

        # Discover tools from provider
        tools = provider.get_available_tools()
        for tool in tools:
            self.registry[tool.name] = tool

    async def execute_tool(
        self,
        tool_name: str,
        parameters: dict
    ) -> ToolResult:
        """Execute a tool call"""

        tool = self.registry.get(tool_name)
        if not tool:
            raise ToolNotFoundError(f"Tool {tool_name} not found")

        provider = self.providers.get(tool.provider_id)
        if not provider:
            raise ProviderNotFoundError(f"Provider {tool.provider_id} not found")

        # Execute
        result = await provider.execute(tool_name, parameters)

        return ToolResult(
            tool_name=tool_name,
            success=result.success,
            output=result.output,
            error=result.error
        )

    async def execute_all(
        self,
        tool_calls: list[ToolCall]
    ) -> list[ToolResult]:
        """Execute multiple tool calls in parallel"""

        tasks = [
            self.execute_tool(call.name, call.parameters)
            for call in tool_calls
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return results
```

#### 6.2.4 Reasoning Orchestrator

```python
class ReasoningOrchestrator:
    """
    Sistema de reasoning iterativo multi-paso

    Responsabilidades:
    - Crear plan de ejecución
    - Ejecutar pasos secuencialmente
    - Resolver dependencias
    - Actualizar estado de ejecución
    """

    def __init__(
        self,
        planner_llm: LLMService,
        executor_llm: LLMService,
        tool_manager: ToolManager
    ):
        self.planner = planner_llm
        self.executor = executor_llm
        self.tools = tool_manager

    async def process_with_reasoning(
        self,
        query: str,
        context: dict
    ) -> AsyncGenerator[ReasoningStep, None]:
        """Process query with iterative reasoning"""

        # Phase 1: Create execution plan
        plan = await self.planner.create_plan(query, context)

        # Phase 2: Execute plan step by step
        resolved_values = {}

        for step in plan.steps:
            # Resolve dependencies
            step_query = self._resolve_placeholders(
                step.query,
                resolved_values
            )

            # Execute step
            if step.type == 'tool_call':
                result = await self.tools.execute_tool(
                    step.tool_name,
                    step.parameters
                )
            elif step.type == 'search':
                result = await self.rag.search(step_query)
            else:  # llm_query
                result = await self.executor.query(step_query)

            # Store result
            resolved_values[step.variable_name] = result

            # Yield progress
            yield ReasoningStep(
                step_number=step.number,
                description=step.description,
                status='completed',
                result=result
            )

        # Phase 3: Final synthesis
        final_answer = await self.executor.synthesize(
            query=query,
            context=resolved_values
        )

        yield ReasoningStep(
            step_number=len(plan.steps) + 1,
            description='Síntesis final',
            status='completed',
            result=final_answer
        )
```

---

## 7. Frontend Architecture

### 7.1 Estructura de Carpetas

```
frontend/
├── index.html
├── package.json (opcional, para dev tools)
│
├── src/
│   ├── main.js                # Entry point
│   │
│   ├── store/                 # State management
│   │   ├── store.js           # Central store
│   │   ├── chat.store.js
│   │   ├── assistant.store.js
│   │   ├── tool.store.js
│   │   └── config.store.js
│   │
│   ├── modules/               # Feature modules
│   │   ├── chat/
│   │   │   ├── chat.component.js
│   │   │   ├── message.component.js
│   │   │   ├── message-input.component.js
│   │   │   └── streaming-message.component.js
│   │   │
│   │   ├── assistants/
│   │   │   ├── assistant-selector.component.js
│   │   │   ├── assistant-gallery.component.js
│   │   │   └── assistant-chip.component.js
│   │   │
│   │   ├── conversations/
│   │   │   ├── conversation-sidebar.component.js
│   │   │   ├── conversation-list.component.js
│   │   │   └── conversation-item.component.js
│   │   │
│   │   ├── references/
│   │   │   ├── reference-badge.component.js
│   │   │   ├── source-panel.component.js
│   │   │   └── source-detail.component.js
│   │   │
│   │   ├── tools/
│   │   │   ├── tool-panel.component.js
│   │   │   ├── tool-execution.component.js
│   │   │   └── tool-config.component.js
│   │   │
│   │   ├── reasoning/
│   │   │   ├── execution-plan.component.js
│   │   │   └── reasoning-step.component.js
│   │   │
│   │   └── config/
│   │       ├── config-popup.component.js
│   │       ├── model-config.component.js
│   │       └── tool-config.component.js
│   │
│   ├── services/              # API clients
│   │   ├── api.service.js     # HTTP client
│   │   ├── websocket.service.js
│   │   ├── storage.service.js
│   │   └── auth.service.js
│   │
│   ├── ui/                    # UI components
│   │   ├── components/
│   │   │   ├── navbar.component.js
│   │   │   ├── sidebar.component.js
│   │   │   ├── modal.component.js
│   │   │   ├── dropdown.component.js
│   │   │   └── tooltip.component.js
│   │   │
│   │   └── templates/
│   │       └── lit-helpers.js
│   │
│   └── utils/                 # Utilities
│       ├── markdown.js
│       ├── validators.js
│       ├── helpers.js
│       └── constants.js
│
├── assets/
│   ├── css/
│   │   ├── main.css
│   │   ├── chat.css
│   │   ├── components.css
│   │   └── themes.css
│   │
│   ├── icons/
│   └── images/
│
└── docs/
    └── components.md
```

### 7.2 State Store (Central)

```javascript
/**
 * Central State Store
 * Single source of truth for application state
 */
class Store {
    constructor() {
        this.state = {
            // Chat state
            currentConversation: null,
            messages: [],
            isStreaming: false,

            // Assistant state
            currentAssistant: null,
            availableAssistants: [],
            tempAssistant: null,  // For @mentions

            // Tools state
            activeTools: [],
            toolResults: {},
            servicesHealth: {},

            // RAG state
            sources: [],
            references: {},

            // Reasoning state
            executionPlan: null,
            reasoningSteps: [],
            reasoningEnabled: true,

            // UI state
            sidebarOpen: false,
            modalOpen: null,
            selectedDevice: null,

            // Config state
            userConfig: {},
            apiKeys: {}
        };

        this.listeners = new Map();
    }

    getState() {
        return { ...this.state };
    }

    setState(updates) {
        this.state = { ...this.state, ...updates };
        this.notify(updates);
    }

    subscribe(key, callback) {
        if (!this.listeners.has(key)) {
            this.listeners.set(key, []);
        }
        this.listeners.get(key).push(callback);

        // Return unsubscribe function
        return () => {
            const callbacks = this.listeners.get(key);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
        };
    }

    notify(updates) {
        Object.keys(updates).forEach(key => {
            const callbacks = this.listeners.get(key) || [];
            callbacks.forEach(cb => cb(this.state[key]));
        });
    }
}

// Singleton instance
export const store = new Store();
```

---

## 8. API Contracts

### 8.1 REST Endpoints

#### Chat

```
POST /api/chat/send
Request:
{
  "conversation_id": "uuid",
  "message": "string",
  "assistant_id": "uuid",
  "device": "string?"
}

Response (SSE Stream):
data: {"type": "token", "content": "Hello"}
data: {"type": "token", "content": " world"}
data: {"type": "sources", "sources": [...]}
data: {"type": "done"}
```

#### WebSocket (Streaming)

```
WS /ws/chat/{conversation_id}

Client → Server:
{
  "type": "message",
  "content": "user message",
  "assistant_id": "uuid"
}

Server → Client:
{
  "type": "token",
  "content": "partial response"
}

{
  "type": "sources",
  "sources": [...]
}

{
  "type": "tool_call",
  "tool": "...",
  "parameters": {...}
}

{
  "type": "done",
  "message_id": "uuid"
}
```

#### Assistants

```
GET /api/assistants
Response: Assistant[]

GET /api/assistants/{id}
Response: Assistant

POST /api/assistants
Request: CreateAssistantRequest
Response: Assistant

PUT /api/assistants/{id}
Request: UpdateAssistantRequest
Response: Assistant

DELETE /api/assistants/{id}
Response: 204 No Content
```

#### Conversations

```
GET /api/conversations
Query: ?limit=50&offset=0
Response: {
  "items": Conversation[],
  "total": number
}

GET /api/conversations/{id}
Response: Conversation

POST /api/conversations
Request: {
  "assistant_id": "uuid",
  "device": "string?"
}
Response: Conversation

DELETE /api/conversations/{id}
Response: 204
```

#### Messages

```
GET /api/conversations/{id}/messages
Query: ?limit=100&offset=0
Response: Message[]

GET /api/messages/{id}
Response: Message
```

#### Tools

```
GET /api/tools
Response: Tool[]

POST /api/tools/execute
Request: {
  "tool_name": "string",
  "parameters": {...}
}
Response: ToolResult

GET /api/tools/providers
Response: ToolProvider[]

POST /api/tools/providers/{id}/health
Response: {
  "status": "healthy|degraded|down",
  "latency_ms": number
}
```

#### Documents

```
POST /api/documents/upload
Content-Type: multipart/form-data
Request:
  file: File
  conversation_id: string

Response: {
  "document_id": "uuid",
  "filename": "string",
  "size_bytes": number,
  "indexed": boolean
}

GET /api/documents/{id}
Response: Document

DELETE /api/documents/{id}
Response: 204
```

#### RAG

```
POST /api/rag/search
Request: {
  "query": "string",
  "top_k": number,
  "filters": {...}
}
Response: Source[]

POST /api/rag/index
Request: {
  "content": "string",
  "metadata": {...}
}
Response: {
  "indexed": boolean,
  "vector_ids": string[]
}
```

---

## 9. Módulos del Sistema

### 9.1 Chat Module

**Responsabilidades:**
- Renderizar mensajes
- Input de usuario
- Streaming de respuestas
- Markdown rendering
- Code syntax highlighting

**Componentes:**
- `ChatComponent` - Container principal
- `MessageComponent` - Renderiza un mensaje
- `MessageInputComponent` - Textarea + botones
- `StreamingMessageComponent` - Muestra tokens en streaming

### 9.2 RAG Module

**Responsabilidades:**
- Búsqueda semántica
- Mostrar referencias `[1][2][3]`
- Panel de fuentes
- Click en referencia → popup

**Componentes:**
- `ReferenceBadgeComponent` - Badge `[n]`
- `SourcePanelComponent` - Lista de fuentes
- `SourceDetailComponent` - Detalle de una fuente

### 9.3 Tools Module

**Responsabilidades:**
- Mostrar tools activas
- Ejecutar tools
- Mostrar resultados
- Health checks

**Componentes:**
- `ToolPanelComponent` - Lista de tools
- `ToolExecutionComponent` - Progreso de ejecución
- `ToolConfigComponent` - Configuración

### 9.4 Reasoning Module

**Responsabilidades:**
- Mostrar plan de ejecución
- Renderizar steps
- Indicadores de estado
- Progreso

**Componentes:**
- `ExecutionPlanComponent` - Panel del plan
- `ReasoningStepComponent` - Un step individual

### 9.5 Assistants Module

**Responsabilidades:**
- Selector de asistente
- Galería de asistentes
- Chip temporal (@mentions)

**Componentes:**
- `AssistantSelectorComponent` - Popover selector
- `AssistantGalleryComponent` - Grid de asistentes
- `AssistantChipComponent` - Chip temporal

---

## 10. Flujos de Datos

### 10.1 Flujo de Chat Normal

```
1. User escribe mensaje
   ↓
2. MessageInputComponent captura
   ↓
3. Store.setState({ isStreaming: true })
   ↓
4. WebSocketService.send(message)
   ↓
5. Backend procesa
   ↓
6. Backend → WebSocket tokens
   ↓
7. StreamingMessageComponent renderiza
   ↓
8. Backend envía sources
   ↓
9. SourcePanelComponent actualiza
   ↓
10. Backend envía done
    ↓
11. Store.setState({ isStreaming: false })
    ↓
12. Message guardado en DB
```

### 10.2 Flujo de RAG

```
1. User envía pregunta
   ↓
2. Backend → RAG Engine
   ↓
3. RAG Engine → ChromaDB search
   ↓
4. ChromaDB → Top K resultados
   ↓
5. RAG Engine → Reranking
   ↓
6. RAG Engine → Extrae referencias
   ↓
7. Backend → LLM con contexto + fuentes
   ↓
8. LLM genera respuesta con [1][2][3]
   ↓
9. Backend → Frontend (sources + message)
   ↓
10. Frontend renderiza con badges clickeables
```

### 10.3 Flujo de Tools

```
1. LLM decide usar tool
   ↓
2. Backend recibe tool_call
   ↓
3. Tool Manager → Provider
   ↓
4. Provider ejecuta (API externa, DB, etc.)
   ↓
5. Provider → Result
   ↓
6. Backend → LLM con result
   ↓
7. LLM continúa generando
   ↓
8. Backend → Frontend
   ↓
9. Frontend muestra tool execution
```

### 10.4 Flujo de Reasoning

```
1. User envía query compleja
   ↓
2. Backend detecta necesidad de reasoning
   ↓
3. Orchestrator → Planner LLM
   ↓
4. Planner crea execution plan (5 steps)
   ↓
5. Backend envía plan → Frontend
   ↓
6. Frontend renderiza ExecutionPlanComponent
   ↓
7. Orchestrator ejecuta step 1
   ↓
8. Backend envía update step 1 → completed
   ↓
9. Frontend actualiza UI (✅)
   ↓
10. Repeat para steps 2-5
    ↓
11. Orchestrator → Final synthesis
    ↓
12. Backend envía respuesta final
```

---

## 11. State Management

### 11.1 Store Pattern

```javascript
// Ejemplo de uso del store

// Subscribe to changes
store.subscribe('currentAssistant', (assistant) => {
    console.log('Assistant changed:', assistant);
    updateUI();
});

// Update state
store.setState({
    currentAssistant: newAssistant,
    tempAssistant: null
});

// Get state
const { messages, isStreaming } = store.getState();
```

### 11.2 State Slices

**Chat State:**
```javascript
{
    currentConversation: Conversation | null,
    messages: Message[],
    isStreaming: boolean,
    streamingMessage: string,
    pendingToolCalls: ToolCall[]
}
```

**Assistant State:**
```javascript
{
    currentAssistant: Assistant | null,
    availableAssistants: Assistant[],
    tempAssistant: Assistant | null,
    originalAssistant: Assistant | null
}
```

**Tools State:**
```javascript
{
    activeTools: Tool[],
    availableProviders: ToolProvider[],
    servicesHealth: Record<string, HealthStatus>,
    toolResults: Record<string, ToolResult>
}
```

**RAG State:**
```javascript
{
    sources: Source[],
    references: Record<number, Source>,
    searchQuery: string | null
}
```

---

## 12. Seguridad

### 12.1 Autenticación

- JWT tokens para API
- HttpOnly cookies
- Refresh tokens

### 12.2 Autorización

- RBAC (Role-Based Access Control)
- User-level permissions
- API key management

### 12.3 Validación

- Input sanitization
- SQL injection prevention
- XSS prevention
- CORS configuration

### 12.4 Encriptación

- API keys encrypted at rest
- TLS for all communications
- Secrets in environment variables

---

## 13. Performance

### 13.1 Backend Optimizations

- **Caching**: Redis para respuestas frecuentes
- **Connection pooling**: DB connections
- **Async everywhere**: Non-blocking I/O
- **Batch processing**: Embeddings en batch

### 13.2 Frontend Optimizations

- **Lazy loading**: Módulos bajo demanda
- **Virtual scrolling**: Para mensajes largos
- **Debouncing**: Input de búsqueda
- **IndexedDB**: Cache local de conversaciones

### 13.3 Streaming

- **Server-Sent Events** o **WebSockets**
- Tokens enviados inmediatamente
- UI actualizada incrementalmente

---

## 14. Deployment

### 14.1 Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/simba
      - REDIS_URL=redis://redis:6379
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis
      - chromadb

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=simba
      - POSTGRES_PASSWORD=simba
      - POSTGRES_DB=simba
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    ports:
      - "6379:6379"

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8001:8000"
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  postgres_data:
  chroma_data:
```

---

## 15. Métricas de Calidad

### 15.1 Code Quality

- **Líneas por función**: < 50
- **Líneas por archivo**: < 500
- **Complejidad ciclomática**: < 10
- **Test coverage**: > 80%

### 15.2 Performance Targets

- **API response time**: < 200ms (p95)
- **Streaming first token**: < 500ms
- **RAG search**: < 1s
- **Tool execution**: < 3s

### 15.3 Reliability

- **Uptime**: 99.9%
- **Error rate**: < 1%
- **Crash-free rate**: > 99.5%

---

## 16. Roadmap

### Phase 1: MVP (Semanas 1-2)
- ✅ Chat core + streaming
- ✅ Asistentes básicos
- ✅ Store centralizado
- ✅ Backend FastAPI
- ✅ ChromaDB integrado

### Phase 2: RAG (Semanas 3-4)
- ✅ RAG engine completo
- ✅ Referencias numeradas
- ✅ Panel de fuentes
- ✅ File upload + indexing

### Phase 3: Tools (Semanas 5-6)
- ✅ Tool manager
- ✅ Provider architecture
- ✅ Confluence, Folder, Jira providers
- ✅ Health monitoring

### Phase 4: Reasoning (Semana 7)
- ✅ Orchestrator
- ✅ Execution plan UI
- ✅ Step-by-step execution

### Phase 5: Advanced UI (Semana 8)
- ✅ @mentions
- ✅ Quick actions
- ✅ Highlighting
- ✅ Data visualization

### Phase 6: Polish (Semana 9)
- ✅ Config completo
- ✅ Export/import
- ✅ Statistics
- ✅ Testing

---

**Documento vivo - Se actualiza con cada cambio arquitectónico significativo**

**Última actualización**: 2024-12-11
**Versión**: 2.0.0
