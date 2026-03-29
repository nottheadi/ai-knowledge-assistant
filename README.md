# AI Knowledge Assistant 🤖

[![Build Status](https://github.com/nottheadi/ai-knowledge-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/nottheadi/ai-knowledge-assistant)
[![License](https://img.shields.io/github/license/nottheadi/ai-knowledge-assistant)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Angular 21+](https://img.shields.io/badge/angular-21+-red.svg)](https://angular.io/)

A modern **Retrieval-Augmented Generation (RAG)** system that enables users to upload documents and query them using natural language. The system intelligently retrieves relevant document chunks and generates context-aware answers using Google Gemini API.

**Built with**: FastAPI (Python) + Angular (TypeScript) + ChromaDB + Google Gemini

---

## ✨ Features

### 📄 Document Management
- Drag-and-drop PDF file upload with validation
- Automatic document processing and chunking
- Persistent storage with ChromaDB vector database
- File deletion and management UI
- Support for documents up to 10MB

### 🤖 AI-Powered Query
- **RAG Mode**: Query your documents with AI for context-aware answers
- **Direct Chat**: Ask general questions without document context
- **Memory-Aware**: Maintains conversation history (last 3 interactions)
- **Source Attribution**: Every RAG answer includes page references and sources
- **Real-time Processing**: Streaming-like responses with markdown formatting

### 🔐 Security & Authentication
- JWT token-based authentication
- Bcrypt password hashing
- Role-based access control (configurable)
- Rate limiting (10 req/min for chat, 5 req/min for uploads)
- Input validation on all endpoints (422 status for invalid data)

### 🎨 User Interface
- Modern, responsive design with Tailwind CSS
- Dark/Light theme toggle
- Real-time chat interface
- File upload progress indication
- Error handling with user-friendly messages

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (3.13 compatible)
- Node.js 18+ with npm
- Google Gemini API key

### 1. Clone & Setup

```bash
# Clone the repository
git clone https://github.com/nottheadi/ai-knowledge-assistant.git
cd ai-knowledge-assistant

# Setup backend
cd apps/backend
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY and JWT_SECRET_KEY

# Setup frontend (in a new terminal)
cd apps/frontend
npm install

# Start both (make sure you have the Makefile)
cd ../..
make run  # Starts both backend and frontend
```

### 2. Access the Application

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

### 3. Default Login Credentials (Development Only)
- **Username**: `admin`
- **Password**: `password123`

> ⚠️ **Security**: Change these credentials before deploying to production!

---

## 📁 Project Structure

```
ai-knowledge-assistant/
├── apps/
│   ├── backend/                    # FastAPI REST API
│   │   ├── app/
│   │   │   ├── main.py            # FastAPI application
│   │   │   ├── config.py          # Configuration & JWT
│   │   │   ├── exceptions.py      # Custom exception classes
│   │   │   ├── routes/            # API endpoints
│   │   │   │   ├── auth.py       # Authentication
│   │   │   │   └── chat.py       # Chat & RAG endpoints
│   │   │   ├── services/          # Business logic
│   │   │   │   ├── llm.py        # Gemini API integration
│   │   │   │   ├── memory.py     # Conversation memory
│   │   │   │   └── user_service.py # User authentication
│   │   │   └── rag/               # RAG pipeline
│   │   │       ├── loader.py      # PDF loading
│   │   │       ├── splitter.py    # Document chunking
│   │   │       ├── embedder.py    # Vector embeddings
│   │   │       ├── vectorstore.py # ChromaDB interface
│   │   │       ├── retriever.py   # Document retrieval
│   │   │       ├── pipeline.py    # Processing pipeline
│   │   │       └── rag_chain.py   # RAG orchestration
│   │   ├── data/                  # User data (JSON)
│   │   ├── chroma_db/             # Vector storage
│   │   ├── uploads/               # Uploaded PDFs
│   │   ├── requirements.txt       # Python dependencies
│   │   └── .env.example           # Environment template
│   │
│   └── frontend/                   # Angular SPA
│       ├── src/
│       │   └── app/
│       │       ├── app.ts         # Root component
│       │       ├── core/          # Services & guards
│       │       │   ├── services/  # API, Auth, Theme
│       │       │   ├── guards/    # Auth guard
│       │       │   └── interceptors/ # HTTP interceptors
│       │       └── features/      # Feature modules
│       │           ├── auth/      # Login page
│       │           └── chat/      # Chat interface
│       ├── angular.json           # Angular config
│       ├── package.json           # NPM dependencies
│       └── environments/          # Environment configs
│
├── docs/                          # Documentation
│   ├── api.md                     # API reference
│   ├── backend.md                 # Backend setup
│   ├── frontend.md                # Frontend setup
│   ├── deployment.md              # Deployment guide
│   ├── development.md             # Development guide
│   ├── contributing.md            # Contributing guidelines
│   └── architecture.md            # Architecture details
│
├── Makefile                       # Common commands
├── pyproject.toml                 # Python project config
├── README.md                      # This file
└── LICENSE                        # MIT License
```

---

## 🔧 Configuration

### Backend (`apps/backend/.env`)

```env
# Google Gemini API
GOOGLE_API_KEY=your-api-key-here

# JWT Authentication
JWT_SECRET_KEY=your-long-secret-key-here-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

### Frontend (`apps/frontend/src/environments/environment.ts`)

```typescript
export const environment = {
  production: false,
  apiBaseUrl: 'http://localhost:8000'
};
```

---

## 📚 Technology Stack

### Backend
| Technology | Purpose | Version |
|-----------|---------|---------|
| **FastAPI** | Web framework | 0.135+ |
| **Uvicorn** | ASGI server | 0.32+ |
| **PyJWT** | JWT authentication | 2.8+ |
| **ChromaDB** | Vector database | 0.4+ |
| **LangChain** | RAG orchestration | 0.1+ |
| **HuggingFace** | Embeddings | 3.0+ |
| **Google Gemini** | LLM API | 0.8+ |

### Frontend
| Technology | Purpose | Version |
|-----------|---------|---------|
| **Angular** | Framework | 21+ |
| **TypeScript** | Language | 5.9+ |
| **RxJS** | Reactive library | 7.8+ |
| **Tailwind CSS** | Styling | 4.1+ |
| **Marked** | Markdown parsing | 17.0+ |

---

## 📖 Documentation

Comprehensive documentation is available in the `/docs` directory:

| Document | Purpose |
|----------|---------|
| **[Backend Setup](docs/backend.md)** | Backend installation, configuration, and development |
| **[Frontend Setup](docs/frontend.md)** | Frontend installation, configuration, and development |
| **[API Reference](docs/api.md)** | Complete API endpoint documentation |
| **[Architecture](docs/architecture.md)** | System design and component overview |
| **[Development Guide](docs/development.md)** | Local development workflow and best practices |
| **[Deployment Guide](docs/deployment.md)** | Production deployment instructions |
| **[Contributing Guide](docs/contributing.md)** | How to contribute to the project |

---

## 🛠️ Common Commands

See [docs/development.md](docs/development.md) for detailed development instructions.

```bash
# Setup
make setup                    # Install all dependencies
make backend-setup           # Backend only
make frontend-setup          # Frontend only

# Development
make run                      # Run both backend & frontend
make backend-run             # Backend only
make frontend-run            # Frontend only

# Testing & Quality
make backend-test            # Run backend tests
make backend-lint            # Lint backend code
make backend-format          # Format backend code
make frontend-lint           # Lint frontend code
make frontend-format         # Format frontend code

# Build
make frontend-build          # Build for production

# Cleanup
make clean                   # Remove all build artifacts
make stop                    # Stop running processes
```

---

## 🔐 Authentication Flow

This application uses JWT (JSON Web Tokens) for secure authentication:

```
1. User enters credentials on login page
2. Frontend sends POST /api/auth/login
3. Backend validates credentials & returns JWT token
4. Frontend stores token in localStorage
5. All subsequent requests include token in Authorization header
6. Backend validates token for protected endpoints
7. On logout, token is cleared from localStorage
```

---

## 🚀 Deployment

### Before Deploying to Production

1. **Security**:
   - [ ] Generate strong JWT_SECRET_KEY
   - [ ] Remove default admin credentials
   - [ ] Update CORS origin from `"*"`
   - [ ] Enable HTTPS only

2. **Configuration**:
   - [ ] Update `.env` with production values
   - [ ] Update frontend API URL
   - [ ] Configure rate limiting appropriately

3. **Database**:
   - [ ] Consider migrating user storage from JSON to PostgreSQL

See [docs/deployment.md](docs/deployment.md) for detailed instructions.

---

## 📊 Performance & Scaling

| Component | Limits | Notes |
|-----------|--------|-------|
| **File Upload** | 10MB | PDF files only |
| **Chat History** | 3 interactions | Configurable in memory.py |
| **Rate Limiting** | 10 req/min (chat) | Configurable in config.py |
| **Token Expiry** | 60 minutes | Configurable in .env |
| **Vector Search** | Full collection | ChromaDB in-memory |

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` when running backend
```bash
# Solution: Ensure all dependencies are installed
pip install -r apps/backend/requirements.txt
```

**Problem**: GOOGLE_API_KEY error
```bash
# Solution: Add GOOGLE_API_KEY to .env
echo "GOOGLE_API_KEY=your-key" >> apps/backend/.env
```

**Problem**: Port 8000 already in use
```bash
# Solution: Kill process or use different port
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9
```

### Frontend Issues

**Problem**: Cannot connect to backend API
- Check backend is running: `curl http://localhost:8000/`
- Check frontend environment config in `environment.ts`
- Verify CORS is enabled in backend

**Problem**: Module not found errors
```bash
# Solution: Reinstall node_modules
cd apps/frontend
rm -rf node_modules package-lock.json
npm install
```

See [docs/faq.md](docs/faq.md) for more FAQs.

---

## 🤝 Contributing

Contributions are welcome! Please see [docs/contributing.md](docs/contributing.md) for:
- Code style guidelines
- Development setup
- Testing requirements
- Pull request process

---

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 👥 Authors & Acknowledgments

- **AI System Architecture Review**: Claude Code (Architecture Review Session)
- **Original Project**: See [CONTRIBUTING.md](docs/contributing.md)

---

## 📞 Support & Questions

- **Issues**: [GitHub Issues](https://github.com/nottheadi/ai-knowledge-assistant/issues)
- **Documentation**: See `/docs` folder
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🗺️ Roadmap

- [ ] Database migration (JSON → PostgreSQL)
- [ ] Docker containerization
- [ ] CI/CD pipeline improvements
- [ ] Advanced vector search features
- [ ] Support for more document formats
- [ ] Batch processing for large documents
- [ ] Multi-user workspace support
- [ ] Document versioning and history

---

**Last Updated**: March 29, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
