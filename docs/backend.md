# Backend Documentation

## Overview

The backend is a RESTful API built with FastAPI that implements a Retrieval-Augmented Generation (RAG) system for document querying and conversational AI.

**Stack**: Python 3.11+ | FastAPI | ChromaDB | Google Gemini | JWT Auth

---

## 🏗️ Architecture

### Core Components

```
apps/backend/
├── app/
│   ├── main.py              # FastAPI application & middleware
│   ├── config.py            # Configuration, JWT, Rate limiting
│   ├── exceptions.py        # Custom exception classes
│   ├── routes/              # API endpoints
│   │   ├── auth.py         # POST /api/auth/login
│   │   └── chat.py         # Chat & RAG endpoints
│   ├── services/            # Business logic layer
│   │   ├── llm.py          # Google Gemini integration
│   │   ├── memory.py       # Conversation memory (last 3 interactions)
│   │   └── user_service.py # User authentication & management
│   └── rag/                 # RAG pipeline modules
│       ├── loader.py        # PDF document loading
│       ├── splitter.py      # Chunk-based document splitting
│       ├── embedder.py      # HuggingFace embeddings
│       ├── vectorstore.py   # ChromaDB interface
│       ├── retriever.py     # Semantic search & retrieval
│       ├── pipeline.py      # Document processing pipeline
│       └── rag_chain.py     # RAG chain orchestration
├── data/
│   └── users.json           # User credentials (JSON file)
├── chroma_db/               # Vector database storage
├── uploads/                 # Uploaded PDF files
├── requirements.txt         # Python dependencies
└── .env.example             # Environment variables template
```

### Data Flow

```
Upload PDF
    ↓
[pipeline.py] → Load → Split → Embed → Store in ChromaDB
    ↓
User Query
    ↓
[rag_chain.py] → Retrieve relevant chunks → Add memory context
    ↓
[llm.py] → Send to Google Gemini → Generate response
    ↓
Return answer + sources + memory update
```

---

## 📦 Installation

### 1. Prerequisites

```bash
python --version  # Should be 3.11 or higher
pip --version     # Should be 21+
```

### 2. Install Dependencies

```bash
cd apps/backend

# Install production dependencies
pip install -r requirements.txt

# (Optional) Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Create Environment File

```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your values
nano .env
```

**Required Variables**:

```env
# Google Gemini API (Required for LLM functionality)
GOOGLE_API_KEY=your-google-gemini-api-key

# JWT Authentication (Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))")
JWT_SECRET_KEY=your-generated-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

---

## 🚀 Running the Backend

### Development Mode

```bash
cd apps/backend

# With auto-reload
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using make command
make backend-run
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production Mode

```bash
# Install gunicorn for production
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --timeout 120 \
  app.main:app
```

---

## 🔐 Authentication

### JWT Token Flow

1. **Login**: `POST /api/auth/login`
   ```bash
   curl -X POST http://localhost:8000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"password123"}'
   ```

2. **Response**: Returns JWT token
   ```json
   {
     "access_token": "eyJhbGc...",
     "token_type": "bearer"
   }
   ```

3. **Use Token**: Add to Authorization header
   ```bash
   curl -H "Authorization: Bearer eyJhbGc..." \
     http://localhost:8000/api/chat/RAG \
     -d '{"query":"..."}'
   ```

### Default Users (Development)

| Username | Password | Role |
|----------|----------|------|
| `admin` | `password123` | Admin |

⚠️ **IMPORTANT**: Change these before deploying to production!

### Add New User (Development)

Edit `apps/backend/data/users.json`:

```json
{
  "users": [
    {
      "id": "1",
      "username": "admin",
      "hashed_password": "$2b$12$...",
      "role": "admin"
    },
    {
      "id": "2",
      "username": "newuser",
      "hashed_password": "$2b$12$...",
      "role": "user"
    }
  ]
}
```

To hash password:
```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("password123")
print(hashed)
```

---

## 📡 API Endpoints

### Authentication

**POST /api/auth/login**
- Login with username/password
- Returns JWT token
- Header: `Content-Type: application/json`

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

### Chat

**POST /api/chat**
- Direct chat (no document context)
- Requires: JWT token in Authorization header

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"What is machine learning?"}'
```

**POST /api/chat/RAG**
- Document-aware chat (retrieval-augmented)
- Uses uploaded documents for context
- Requires: JWT token
- Returns: Answer + source attributions

```bash
curl -X POST http://localhost:8000/api/chat/RAG \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Summarize the document"}'
```

### File Management

**POST /api/upload**
- Upload PDF document (max 10MB)
- Requires: JWT token
- Content-Type: multipart/form-data

```bash
curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

**GET /api/uploads**
- List all uploaded files
- Requires: JWT token

```bash
curl http://localhost:8000/api/uploads \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**DELETE /api/uploads/{filename}**
- Delete uploaded file
- Requires: JWT token

```bash
curl -X DELETE http://localhost:8000/api/uploads/document.pdf \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Health

**GET /**
- API health check
- No authentication required

```bash
curl http://localhost:8000/
```

---

## ⚙️ Configuration

### Rate Limiting (`app/config.py`)

Default limits:
- Chat endpoints: **10 requests/minute**
- Upload endpoint: **5 requests/minute**

To update:
```python
# In app/config.py
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10/minute"]
)

# On routes
@router.post("/chat", dependencies=[Depends(limiter.limit("10/minute"))])
```

### CORS Configuration (`app/main.py`)

Currently allows all origins (`"*"`). For production:

```python
CORSMiddleware(
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET", "DELETE"],
    allow_headers=["*"],
)
```

### Conversation Memory (`app/services/memory.py`)

Stores last 3 interactions. To change:

```python
# In memory.py
MAX_MEMORY_INTERACTIONS = 3  # Change this value
```

---

## 🧪 Testing

### Run Tests

```bash
make backend-test

# Or with pytest directly
cd apps/backend
pytest tests/ -v
```

### Run Specific Test

```bash
pytest tests/test_routes_chat.py::test_chat_rag -v
```

### Test with Coverage

```bash
pytest tests/ --cov=app --cov-report=html
```

---

## 📊 Code Quality

### Linting

```bash
# Check code style
make backend-lint

# Or with flake8
flake8 app/
```

### Formatting

```bash
# Format code
make backend-format

# Or manually
black app/
isort app/
```

### Type Checking (Optional)

```bash
mypy app/ --ignore-missing-imports
```

---

## 📝 RAG Pipeline Details

### 1. Document Loading (`rag/loader.py`)

- Loads PDF files using PyPDF
- Extracts text and metadata
- Validates PDF format

### 2. Document Splitting (`rag/splitter.py`)

- Splits documents into chunks (default: 1000 chars, 200 overlap)
- Maintains semantic coherence
- Preserves metadata (page numbers, sources)

### 3. Embedding (`rag/embedder.py`)

- Uses HuggingFace `sentence-transformers`
- Model: `all-MiniLM-L6-v2` (lightweight, fast)
- Generates 384-dimensional vectors

### 4. Vector Store (`rag/vectorstore.py`)

- ChromaDB for persistent storage
- Stores embeddings + text + metadata
- Located in `chroma_db/` directory

### 5. Retrieval (`rag/retriever.py`)

- Semantic search using cosine similarity
- Returns top-k most relevant chunks (default: 3)
- Includes source metadata

### 6. RAG Chain (`rag/rag_chain.py`)

- Orchestrates entire RAG flow
- Adds conversation memory context
- Formats prompt for LLM
- Handles errors gracefully

---

## 🔧 Troubleshooting

### API Won't Start

**Problem**: `Address already in use`
```bash
# Kill process on port 8000
lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001
```

**Problem**: `ModuleNotFoundError`
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

**Problem**: `GOOGLE_API_KEY not set`
```bash
# Check .env file
cat apps/backend/.env

# Should contain: GOOGLE_API_KEY=your-key
# If missing, add it and restart
```

### JWT Token Issues

**Problem**: `Invalid token` error
```bash
# Token expired - login again
curl -X POST http://localhost:8000/api/auth/login \
  -d '{"username":"admin","password":"password123"}'

# Use the new token
```

**Problem**: `JWT_SECRET_KEY not set` warning
```bash
# Generate a new secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Add to .env
echo "JWT_SECRET_KEY=<generated-key>" >> apps/backend/.env
```

### ChromaDB Issues

**Problem**: Vector database corrupted
```bash
# Backup and remove old database
mv chroma_db chroma_db.backup

# Restart - new database will be created
uvicorn app.main:app --reload
```

---

## 📚 Dependencies

See `requirements.txt` for complete list:

```
fastapi==0.135.1           # Web framework
uvicorn[standard]==0.32.0  # ASGI server
google-generativeai==0.8.0 # Gemini API
chromadb==0.4.24          # Vector database
langchain==0.1.20         # RAG orchestration
sentence-transformers==3.0.1  # Embeddings
PyPDF==6.9.1              # PDF loading
PyJWT==2.10.1             # JWT tokens
passlib[bcrypt]==1.7.4    # Password hashing
slowapi==0.1.9            # Rate limiting
```

For development:
```
pytest==7.4.0             # Testing
black==23.0.0             # Code formatting
flake8==6.0.0             # Linting
isort==5.12.0             # Import sorting
```

---

## 🚀 Deployment

### Docker (Recommended)

```bash
# Build image
docker build -f Dockerfile.backend -t aka-backend:latest .

# Run container
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=your-key \
  -e JWT_SECRET_KEY=your-secret \
  aka-backend:latest
```

### Heroku/Railway

```bash
# Procfile needed
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app" > Procfile

# Deploy with git
git push heroku main
```

See [docs/deployment.md](deployment.md) for detailed deployment options.

---

## 📖 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Google Gemini API](https://cloud.google.com/vertex-ai/docs/generative-ai/models/gemini)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/rfc7519)

---

**Last Updated**: March 29, 2026
**Status**: Production Ready ✅
