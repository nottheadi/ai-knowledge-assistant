
# AI Knowledge Assistant


![Build Status](https://github.com/nottheadi/ai-knowledge-assistant/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/nottheadi/ai-knowledge-assistant)
![License](https://img.shields.io/github/license/nottheadi/ai-knowledge-assistant)

## Quickstart

1. Clone the repo: `git clone https://github.com/nottheadi/ai-knowledge-assistant.git`
2. Install dependencies: `pip install -r backend/requirements.txt`
3. Set up `.env` in backend/ (see below for variables)
4. Run: `cd backend && uvicorn app.main:app --reload`
5. Access API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Tech Stack

- Python 3.12, FastAPI, Uvicorn
- Google Gemini API (LLM)
- ChromaDB, LangChain, HuggingFace sentence-transformers
- Pytest, Black, Flake8, isort, mypy, pre-commit


This is an AI-enabled assistant that responds to queries related to uploaded documents (PDFs, Confluence, SOPs, etc.).

## Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Developer Guide](docs/developer_guide.md)

See the `docs/` folder for more details and to contribute to project documentation.

## Features

- Upload and process PDF documents
- Query AI models (Google Gemini) for answers based on your documents
- REST API built with FastAPI

## Setup

1. **Install dependencies:**
	```sh
	pip install -r backend/requirements.txt
	```

2. **Set environment variables:**
    - `GEMINI_API_KEY`: Your Google Gemini API key
    - `MODEL`: The Gemini model name (e.g., `gemini-pro`)

	You can use a `.env` file in the backend directory. Example:
	```env
	GEMINI_API_KEY=your-key-here
	MODEL=gemini-pro
	```

3. **Run the app:**
    ```sh
    cd backend
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

4. **Access the API:**
    - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    - Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

See [API Documentation](docs/api.md) for details on endpoints, requests, and responses.

### RAG Chat

- `POST /api/chat/RAG`
  
	**Request JSON:**
	```json
	{"query": "Summarize the uploaded document."}
	```
	**Response JSON:**
	```json
	{"answer": "...", "sources": [ ... ]}
	```

### Upload PDF

- `POST /api/upload`
  
	**Form Data:**
	- `file`: PDF file to upload (max 10MB)
  
	**Response JSON:**
	```json
	{"message": "File uploaded and processed successfully."}
	```
  
	**Errors:**
	- Only PDF files are allowed
	- File size exceeds 10MB
	- Invalid PDF signature

## Testing

Run all tests:
```
pytest tests/
```

## Security Notes
- Only PDF files are accepted for upload
- File size is limited to 10MB
- Uploaded files are checked for valid PDF signature

---
For more details, see the code and tests in the repository.
