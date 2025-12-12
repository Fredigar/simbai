# 🤖 SIMBA

**Sistema Inteligente de Mensajería con Backend Avanzado**

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## 📋 Descripción

SIMBA es una plataforma de chat avanzada con capacidades de IA que combina múltiples proveedores de LLM (OpenAI, Anthropic) con Retrieval-Augmented Generation (RAG) para conversaciones inteligentes y contextualmente relevantes.

### ✨ Características Principales

- 🤖 **Multi-LLM Support**: OpenAI GPT-4 y Anthropic Claude
- 📚 **RAG (Retrieval-Augmented Generation)**: Búsqueda semántica con ChromaDB
- 📄 **File Processing**: Extracción de texto de PDF, DOCX, TXT
- 💬 **Streaming**: Respuestas en tiempo real con SSE
- 🎭 **Multiple Assistants**: 4 asistentes con personalidades diferentes
- 🗄️ **Database**: PostgreSQL/SQLite con migraciones Alembic
- 🔍 **Semantic Search**: Vector embeddings para búsqueda inteligente

---

## 🚀 Inicio Rápido

### Opción 1: Chat CLI Interactivo (Más Fácil)

```bash
cd backend
python scripts/chat_cli.py
```

✅ Funciona sin API keys (modo demo)
✅ Streaming palabra por palabra
✅ 4 asistentes para elegir

### Opción 2: API REST Server

```bash
cd backend
python main.py
# o
uvicorn app.main:app --reload --port 8000
```

### Opción 3: Con LLM Real

```bash
cd backend

# Crear archivo .env
cat > .env << EOF
OPENAI_API_KEY=sk-tu-key-aqui
# o
ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
EOF

# Ejecutar
python scripts/chat_cli.py
```

---

## 📦 Instalación

### Requisitos

- Python 3.11+
- pip

### Instalar Dependencias

```bash
cd backend
pip install -r requirements.txt
```

### Inicializar Base de Datos

```bash
# Ejecutar migraciones
alembic upgrade head

# Crear datos de prueba
python scripts/seed_data.py
```

---

## 🏗️ Arquitectura

```
backend/
├── app/
│   ├── main.py                    # FastAPI application
│   ├── config.py                  # Configuration
│   ├── api/routes/                # API endpoints
│   │   ├── chat.py               # Chat API
│   │   ├── rag.py                # RAG API
│   │   └── documents.py          # Document API
│   ├── services/
│   │   ├── llm/                  # LLM clients
│   │   ├── rag/                  # RAG services
│   │   ├── file_processing/      # File extractors
│   │   └── chat_service.py       # Chat orchestration
│   ├── models/                    # Pydantic schemas
│   ├── db/
│   │   ├── models.py             # SQLAlchemy ORM
│   │   ├── session.py            # Database session
│   │   └── chroma_client.py      # ChromaDB client
│   ├── repositories/              # Data access layer
│   └── utils/                     # Utilities
├── alembic/                       # Database migrations
├── scripts/                       # Utility scripts
└── requirements.txt
```

---

## 🌐 API Endpoints

### Chat API (`/chat`)

```
POST   /chat/send                        # Enviar mensaje (non-streaming)
POST   /chat/stream                      # Enviar mensaje (streaming)
POST   /chat/conversations               # Crear conversación
GET    /chat/conversations/{id}/messages # Obtener mensajes
```

### RAG API (`/rag`)

```
POST   /rag/index                        # Indexar documento
POST   /rag/search                       # Búsqueda semántica
DELETE /rag/documents/{id}               # Eliminar vectores
```

### Documents API (`/documents`)

```
POST   /documents/upload                 # Subir archivo
GET    /documents/conversation/{id}      # Listar documentos
GET    /documents/{id}                   # Obtener documento
DELETE /documents/{id}                   # Eliminar documento
```

### System API

```
GET    /                                 # Info de la aplicación
GET    /health                           # Health check
```

---

## 🧪 Tests

```bash
cd backend

# Tests de infraestructura (sin API keys)
python scripts/test_database.py
python scripts/test_chat_mock.py

# Tests con LLM real (requiere API keys)
python scripts/test_chat.py

# Demo completo
python scripts/demo_complete.py
```

---

## 📚 Documentación

- **[PROJECT_STATUS.md](backend/PROJECT_STATUS.md)**: Estado completo del proyecto
- **[CHAT_CLI_README.md](backend/CHAT_CLI_README.md)**: Guía del CLI interactivo
- **[SIMBA_ARCHITECTURE.md](SIMBA_ARCHITECTURE.md)**: Arquitectura detallada del sistema
- **[specifications.md](specifications.md)**: Especificaciones originales

---

## 🔧 Configuración

### Variables de Entorno

Crear archivo `backend/.env`:

```env
# Application
DEBUG=True
LOG_LEVEL=INFO

# Database
DATABASE_URL=sqlite+aiosqlite:///./simba.db

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8001
```

---

## 🎯 Características Implementadas

### ✅ Phase 1: Foundation
- Configuración con Pydantic Settings
- Logging estructurado (structlog)
- Excepciones personalizadas
- Docker Compose setup

### ✅ Phase 2: Data Models & Database
- Modelos Pydantic y SQLAlchemy
- Repository Pattern
- Migraciones Alembic
- 4 asistentes pre-configurados

### ✅ Phase 3: Chat Service & LLM Integration
- OpenAI GPT-4 client
- Anthropic Claude client
- Streaming con SSE
- Context management

### ✅ Phase 4: RAG Engine
- Embeddings con sentence-transformers
- ChromaDB integration
- Semantic search
- Source reranking

### ✅ Phase 7: File Processing
- PDF extraction (PyMuPDF)
- DOCX extraction (python-docx)
- Auto-indexing para RAG

---

## 🤝 Contribuir

Este proyecto está en desarrollo activo. Para contribuir:

1. Fork el repositorio
2. Crea una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Add: nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📝 Licencia

MIT License - ver archivo LICENSE para detalles

---

## 👥 Autores

- **Desarrollo inicial**: Claude + Fredigar
- **Arquitectura**: Basada en especificaciones detalladas

---

## 🔗 Enlaces

- [Documentación completa](backend/PROJECT_STATUS.md)
- [Guía de uso del CLI](backend/CHAT_CLI_README.md)
- [Arquitectura del sistema](SIMBA_ARCHITECTURE.md)

---

**¿Preguntas o problemas?** Abre un issue en GitHub.
