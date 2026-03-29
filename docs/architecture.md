# Architecture Overview

Complete technical architecture of the AI Knowledge Assistant system.

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Angular SPA (Frontend)                        │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  Login Component  │  Chat Component  │  File Upload  │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  Services Layer                                      │ │ │
│  │  │  ├─ API Service → HTTP Calls                         │ │ │
│  │  │  ├─ Auth Service → JWT Management                    │ │ │
│  │  │  └─ Theme Service → Dark/Light Mode                  │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ HTTP/REST (JSON)
                   │
┌──────────────────▼──────────────────────────────────────────────┐
│                      FASTAPI SERVER                             │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                   HTTP Routes                              │ │
│  │  ├─ POST /api/auth/login      (JWT Auth)                 │ │
│  │  ├─ POST /api/chat            (Direct Chat)              │ │
│  │  ├─ POST /api/chat/RAG        (Document Query)           │ │
│  │  ├─ POST /api/upload          (File Upload)              │ │
│  │  ├─ GET  /api/uploads         (List Files)               │ │
│  │  └─ DELETE /api/uploads/{id}  (Delete File)              │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Business Logic Layer                          │ │
│  │  ┌──────────────────┐  ┌──────────────────┐               │ │
│  │  │  User Service    │  │  LLM Service     │               │ │
│  │  │  (Auth)          │  │  (Gemini API)    │               │ │
│  │  └──────────────────┘  └──────────────────┘               │ │
│  │  ┌──────────────────┐                                      │ │
│  │  │  Memory Service  │                                      │ │
│  │  │  (Conversation   │                                      │ │
│  │  │   Context)       │                                      │ │
│  │  └──────────────────┘                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │               RAG Pipeline Layer                           │ │
│  │  ┌──────────────────────────────────────────────────────┐ │ │
│  │  │  1. Loader       → Load & parse PDF                 │ │ │
│  │  │  2. Splitter     → Split into chunks                │ │ │
│  │  │  3. Embedder     → Generate vectors (HuggingFace)   │ │ │
│  │  │  4. Vectorstore  → Store in ChromaDB                │ │ │
│  │  │  5. Retriever    → Find relevant chunks             │ │ │
│  │  │  6. RAG Chain    → Orchestrate process              │ │ │
│  │  └──────────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ▼          ▼          ▼
   ┌─────────┐ ┌────────┐ ┌──────────┐
   │ChromaDB │ │Gemini  │ │File      │
   │Vector   │ │LLM API │ │System    │
   │Database │ │        │ │(Uploads) │
   └─────────┘ └────────┘ └──────────┘
```

---

## 🔄 Data Flow

### Document Upload Flow

```
User selects PDF
     ↓
Frontend validates (type, size)
     ↓
Frontend sends to POST /api/upload
     ↓
Backend validates file
     ↓
[Loader] - Extract text from PDF
     ↓
[Splitter] - Split into chunks (1000 chars, 200 overlap)
     ↓
[Embedder] - Generate embeddings (HuggingFace All-MiniLM)
     ↓
[Vectorstore] - Store in ChromaDB with metadata
     ↓
Return success to frontend
```

### Chat Query Flow

```
User types query
     ↓
Frontend validates (1-5000 chars)
     ↓
Frontend adds Authorization header (JWT token)
     ↓
POST /api/chat/RAG with query
     ↓
Backend validates JWT token
     ↓
[Retriever] - Find top 3 relevant chunks from ChromaDB
     ↓
[Memory Service] - Get last 3 interactions
     ↓
[RAG Chain] - Combine documents + memory + query
     ↓
[LLM Service] - Send prompt to Google Gemini
     ↓
Parse response + extract sources
     ↓
Update memory with new interaction
     ↓
Return answer + sources to frontend
     ↓
Frontend renders markdown response
```

### Authentication Flow

```
User visits app
     ↓
Frontend checks localStorage for JWT token
     ↓
If token exists:
  → Validate with backend
  → If valid → Show chat
  → If expired → Redirect to login
     ↓
User enters credentials
     ↓
POST /api/auth/login
     ↓
Backend hashes password with bcrypt
     ↓
Compare with stored hash in users.json
     ↓
If match:
  → Generate JWT token
  → Return token
     ↓
Frontend stores in localStorage
     ↓
Auth Interceptor adds to all requests
     ↓
Redirect to chat
```

---

## 🧩 Component Details

### Frontend Components

#### Root Component (app.ts)

- **Responsibility**: Orchestrate main features
- **Manages**: Chat state, file list, loading states
- **Uses**: ApiService, AuthService, ThemeService
- **Issues**: Currently too large (210 lines) - candidate for refactoring

#### Login Component

- **Path**: `features/auth/pages/login/`
- **Responsibility**: User authentication
- **Features**: Username/password form, error display, loading state
- **Uses**: AuthService

#### Chat Components

1. **MessageListComponent**: Display chat history
2. **MessageBubbleComponent**: Individual message display
3. **ChatInputComponent**: Message input and submission

### Backend Routes

#### Auth Routes (`routes/auth.py`)

- `POST /api/auth/login`: Login endpoint
  - Validates credentials
  - Generates JWT token
  - Returns token to client

#### Chat Routes (`routes/chat.py`)

- `POST /api/chat`: Direct chat (no documents)
  - Validates query length
  - Calls LLM service directly
  - Returns response

- `POST /api/chat/RAG`: RAG-based chat
  - Validates JWT token
  - Retrieves relevant documents
  - Gets conversation memory
  - Calls RAG chain
  - Returns answer + sources

- `POST /api/upload`: Upload PDF
  - Validates file (type, size)
  - Processes document through RAG pipeline
  - Stores in ChromaDB
  - Returns success

- `GET /api/uploads`: List uploaded files
  - Returns list of file names
  - Requires JWT token

- `DELETE /api/uploads/{filename}`: Delete file
  - Removes file from filesystem
  - Removes embeddings from ChromaDB
  - Updates memory

### Services Layer

#### User Service (`services/user_service.py`)

- Manages user authentication
- Loads users from JSON file
- Validates credentials with bcrypt
- Used by auth routes

#### LLM Service (`services/llm.py`)

- Interfaces with Google Gemini API
- Generates responses from prompts
- Handles API errors gracefully
- Logs all API calls

#### Memory Service (`services/memory.py`)

- Stores conversation history
- Maintains last 3 interactions
- Formats as context for LLM
- Clears on file deletion

### RAG Pipeline Modules

1. **Loader** (`rag/loader.py`)
   - Loads PDF files
   - Extracts text content
   - Preserves page information

2. **Splitter** (`rag/splitter.py`)
   - Chunks documents (1000 chars)
   - Maintains overlap (200 chars)
   - Preserves semantic boundaries

3. **Embedder** (`rag/embedder.py`)
   - Uses HuggingFace `all-MiniLM-L6-v2`
   - Generates 384-dimensional vectors
   - Cached for performance

4. **Vectorstore** (`rag/vectorstore.py`)
   - ChromaDB interface
   - Stores embeddings + text + metadata
   - Supports similarity search

5. **Retriever** (`rag/retriever.py`)
   - Performs semantic search
   - Returns top-k results (k=3)
   - Includes source metadata

6. **Pipeline** (`rag/pipeline.py`)
   - Orchestrates loading → splitting → embedding
   - Error handling and logging
   - Transaction-like processing

7. **RAG Chain** (`rag/rag_chain.py`)
   - Main orchestration
   - Combines retrieval + memory + LLM
   - Formats final response

---

## 📊 Database Schema

### Users (JSON File - `data/users.json`)

```json
{
  "users": [
    {
      "id": "1",
      "username": "admin",
      "hashed_password": "$2b$12$...",
      "role": "admin"
    }
  ]
}
```

### ChromaDB Collections

**Documents Collection**:
- Document name: `[filename]`
- Chunks with metadata:
  ```python
  {
    "id": "chunk_1",
    "embedding": [0.1, 0.2, ...],  # 384-dim vector
    "document": "chunk text content",
    "metadata": {
      "source": "document.pdf",
      "page": 1,
      "chunk_index": 1
    }
  }
  ```

### Conversation Memory (In-Memory)

```python
memory = {
  "interactions": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."},
    # ... last 3 interactions
  ]
}
```

---

## 🔐 Security Model

### Authentication

- JWT tokens issued on login
- Tokens expire after 60 minutes
- All protected endpoints validate token
- Passwords hashed with bcrypt

### Authorization

- JWT payload contains `sub` (user_id) and `username`
- Currently supports basic user/admin distinction
- Extensible for role-based access control

### Input Validation

- Query length: 1-5000 characters
- File type: PDF only
- File size: Max 10MB
- All inputs validated at route level (422 response)

### Rate Limiting

- `/api/chat`: 10 requests/minute
- `/api/chat/RAG`: 10 requests/minute
- `/api/upload`: 5 requests/minute
- Returns 429 if limit exceeded

---

## 📈 Performance Considerations

### Frontend

- **Change Detection**: OnPush for components
- **Lazy Loading**: Auth feature lazy-loaded
- **Signal-based**: Reactive state management
- **No Memory Leaks**: `takeUntilDestroyed()` pattern

### Backend

- **Rate Limiting**: Prevents abuse
- **Connection Pooling**: Reuse HTTP connections
- **Embedding Cache**: HuggingFace embeddings cached
- **Async Operations**: All I/O is async

### Vector Search

- **Approximate Search**: ChromaDB uses efficient similarity
- **In-Memory**: Entire dataset in memory (suitable for small-medium docs)
- **Scalability**: Strategy for migration to production database

---

## 🔄 Future Architecture Changes

### Phase 1: Component Refactoring (Next Sprint)

- Extract `FileManagementComponent`
- Create `ChatService`
- Create `FileManagementService`
- Reduce god component complexity

### Phase 2: Type Safety (1-2 weeks)

- Create TypeScript models for all API responses
- Remove `any` types
- Add proper error types

### Phase 3: Database Migration (1 month)

- Migrate from JSON to PostgreSQL
- User management via ORM
- Better scalability

### Phase 4: Containerization (Ongoing)

- Docker support
- Docker Compose for local dev
- Kubernetes for production

---

## 🏢 Deployment Architecture

### Development

```
Laptop/Local Machine
├── Frontend (npm serve on :4200)
├── Backend (uvicorn on :8000)
├── ChromaDB (chroma_db/)
└── Users (data/users.json)
```

### Production

```
Cloud Provider (AWS/Heroku/Railway)
├── Load Balancer (SSL/TLS)
├── Nginx Reverse Proxy
├── Gunicorn + Uvicorn (Backend)
├── Node HTTP Server (Frontend)
├── PostgreSQL (User DB)
├── Redis (Session/Cache - optional)
└── Object Storage (Uploads - S3/GCS - optional)
```

---

## 🔗 Technology Choices

### Why FastAPI?

- Built-in async support
- Automatic API documentation (Swagger/ReDoc)
- Type validation with Pydantic
- Fast execution
- Easy JWT integration

### Why Angular?

- Strong typing with TypeScript
- Powerful CLI and tooling
- Great for large SPAs
- Built-in dependency injection
- Excellent documentation

### Why ChromaDB?

- Purpose-built for embeddings
- Simple HTTP API
- Persistent local storage
- Easy to upgrade to production versions
- Good Python support

### Why Google Gemini?

- State-of-the-art language model
- Accessible API
- Good documentation
- Competitive pricing

---

## 📝 Configuration Management

### Environment Variables

```env
# Backend (.env)
GOOGLE_API_KEY=...          # Google Gemini
JWT_SECRET_KEY=...          # JWT signing
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

### Feature Toggles

- In `config.py`:
  - `JWT_EXPIRE_MINUTES`: Token lifetime
  - `limiter.limit()`: Rate limits per endpoint
  - In `memory.py`: `MAX_MEMORY_INTERACTIONS`

### Build Configuration

- Frontend: `environment.ts` & `environment.prod.ts`
- Backend: `.env` file

---

**Last Updated**: March 29, 2026
**Status**: Current ✅
