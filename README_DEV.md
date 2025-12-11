# SIMBA - Development Guide

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Node.js 18+ (optional, for dev tools)

### Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd simbai
```

2. **Backend Setup**
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

3. **Start with Docker Compose** (Recommended)
```bash
# From project root
docker-compose up -d

# Check logs
docker-compose logs -f backend
```

4. **Or run locally**
```bash
# Backend
cd backend
python main.py

# Frontend (separate terminal)
cd frontend
python3 -m http.server 3000
```

### Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **ChromaDB**: http://localhost:8001

## 📁 Project Structure

See [SIMBA_ARCHITECTURE.md](./SIMBA_ARCHITECTURE.md) for complete architecture documentation.

```
simba/
├── backend/           # Python FastAPI backend
├── frontend/          # Lit HTML + Framework7 frontend
├── docker-compose.yml # Docker orchestration
└── SIMBA_ARCHITECTURE.md  # Complete architecture docs
```

## 🛠️ Development Workflow

### Backend Development

```bash
cd backend

# Run with auto-reload
python main.py

# Run tests
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/
```

### Frontend Development

```bash
cd frontend

# Serve locally
python3 -m http.server 3000

# Or with Node.js
npm run dev
```

## 📋 Phase 1 Implementation Status

- [x] Project structure
- [x] Configuration management
- [x] Logging & exceptions
- [x] Validation utilities
- [ ] Data models (Pydantic)
- [ ] Database setup (SQLAlchemy + ChromaDB)
- [ ] ChatService basic
- [ ] API routes
- [ ] Frontend store
- [ ] Chat UI components

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/unit/test_config.py
```

## 📚 Documentation

- [SIMBA_ARCHITECTURE.md](./SIMBA_ARCHITECTURE.md) - Complete system architecture
- [specifications.md](./specifications.md) - Feature specifications
- Backend API docs: http://localhost:8000/api/docs

## 🐛 Troubleshooting

### ChromaDB connection issues
```bash
# Check if ChromaDB is running
curl http://localhost:8001/api/v1/heartbeat

# Restart ChromaDB
docker-compose restart chromadb
```

### Database issues
```bash
# Reset database
rm simba.db
python -c "from app.db.base import init_db; init_db()"
```

## 📞 Support

For issues or questions, check:
- Architecture docs
- API documentation
- GitHub issues

---

**Status**: Phase 1 - Foundation Setup ✅
**Next**: Data Models & Database Setup
