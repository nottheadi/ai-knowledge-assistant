

# AI Knowledge Assistant (Monorepo)


![Build Status](https://github.com/nottheadi/ai-knowledge-assistant/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/nottheadi/ai-knowledge-assistant)
![License](https://img.shields.io/github/license/nottheadi/ai-knowledge-assistant)


## Quickstart

1. Clone the repo: `git clone https://github.com/nottheadi/ai-knowledge-assistant.git`
2. Install backend dependencies: `pip install -r apps/backend/requirements.txt`
3. (Optional) Install frontend dependencies: `cd apps/frontend && npm install`
4. Set up `.env` in `apps/backend/` (see below for variables)
5. Run backend: `cd apps/backend && uvicorn app.main:app --reload`
6. (Optional) Run frontend: `cd apps/frontend && npm start` (Angular dev server)
7. Access API docs: [http://localhost:8000/docs](http://localhost:8000/docs)


## Tech Stack

**Backend:**
- Python 3.12, FastAPI, Uvicorn
- Google Gemini API (LLM)
- ChromaDB, LangChain, HuggingFace sentence-transformers
- Pytest, Black, Flake8, isort, mypy, pre-commit

**Frontend:**
- Angular 17 (TypeScript)
- RxJS, Angular Material (optional)

AI Knowledge Assistant is a Retrieval-Augmented Generation (RAG) system that enables users to upload documents and query them using natural language. The system retrieves relevant document chunks using vector embeddings and generates context-aware answers using a large language model. The monorepo structure contains both backend and frontend apps under `apps/`.



## Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Developer Guide](docs/developer_guide.md)

**Key Backend Endpoints:**
- `POST /api/chat/RAG` — Query documents with Retrieval-Augmented Generation (JSON body: `{ "query": "..." }`)
- `GET /api/uploads` — List all uploaded PDF files
- `POST /api/upload` — Upload a PDF file

See the `docs/` folder for more details and to contribute to project documentation.


## Monorepo Architecture Overview

```
ai-knowledge-assistant/
├── apps/
│   ├── backend/   # FastAPI backend (RAG, ChromaDB, Gemini LLM)
│   └── frontend/  # Angular frontend (UI, chat, upload)
├── docs/          # Documentation
└── ...            # Project root files
```

### Backend Data Flow

1. User uploads a PDF via `/api/upload`
2. PDF is loaded, split, embedded, and stored in ChromaDB
3. User queries `/api/chat/RAG` with a question
4. Relevant chunks are retrieved from ChromaDB
5. Chunks and conversation memory are sent to Gemini LLM
6. LLM generates an answer with sources

### Frontend
- Angular SPA for uploading PDFs, listing files, and chatting with the AI (RAG and standard chat modes)
- Communicates with backend via REST API


## Features

**Backend:**
- Upload and process PDF documents
- Query AI models (Google Gemini) for answers based on your documents
- REST API built with FastAPI
- Conversational memory: The assistant uses the last 3 chat interactions for context
- RAG responses include detailed source metadata (page, source) for each answer

**Frontend:**
- Drag & drop or select PDF files to upload
- View a list of uploaded PDFs
- Chat interface for asking questions and receiving answers
- RAG chat mode for document-aware answers

## Setup

### Backend
1. **Install dependencies:**
	```sh
	pip install -r apps/backend/requirements.txt
	```
2. **Set environment variables:**
	- `GEMINI_API_KEY`: Your Google Gemini API key
	- `MODEL`: The Gemini model name (e.g., `gemini-pro`)
	- Use a `.env` file in `apps/backend/`:
	  ```env
	  GEMINI_API_KEY=your-key-here
	  MODEL=gemini-pro
	  ```
3. **Run the backend:**
	```sh
	cd apps/backend
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	```
4. **Access the API:**
	- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
	- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Frontend (optional)
1. **Install dependencies:**
	```sh
	cd apps/frontend
	npm install
	```
2. **Run the frontend:**
	```sh
	npm start
	```
	- Access the UI at [http://localhost:4200/](http://localhost:4200/)
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)


## API Endpoints

See [API Documentation](docs/api.md) for details on endpoints, requests, and responses.

### RAG Chat

- `POST /api/chat/RAG`
    - **Request JSON:** `{ "query": "Summarize the uploaded document." }`
    - **Response JSON:** `{ "answer": "...", "sources": [ ... ] }`

### Upload PDF

- `POST /api/upload`
    - **Form Data:** `file` (PDF, max 10MB)
    - **Response JSON:** `{ "message": "File uploaded and processed successfully." }`
    - **Errors:** Only PDF files, max 10MB, valid PDF signature


## Testing

### Backend
Run all backend tests:
```sh
cd apps/backend
pytest tests/
```

### Frontend
Run frontend unit tests:
```sh
cd apps/frontend
npm test
```


## Security Notes
- Only PDF files are accepted for upload
- File size is limited to 10MB
- Uploaded files are checked for valid PDF signature

---

For more details, see the code and tests in the repository.
