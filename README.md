# AI Knowledge Assistant

This is an AI-enabled assistant that responds to queries related to uploaded documents (PDFs, Confluence, SOPs, etc.).

## Features

- Upload and process PDF documents
- Query AI models (Google Gemini) for answers based on your documents
- REST API built with FastAPI

## Setup

1. **Install dependencies:**
	```
	pip install -r backend/requirement.txt
	```

2. **Set environment variables:**
	- `GEMINI_API_KEY`: Your Google Gemini API key
	- `MODEL`: The Gemini model name (e.g., `gemini-pro`)

	You can use a `.env` file in the backend directory.

3. **Run the app:**
	```
	cd backend
	/home/codespace/.python/current/bin/python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
	```

4. **Access the API:**
	- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
	- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## API Endpoints

### Health Check

- `GET /` — Returns API status.
  
	**Response:**
	```json
	{"status": "success", "message": "AI Knowledge Assistant API is running."}
	```

### Chat with AI

- `POST /api/chat`
  
	**Request JSON:**
	```json
	{"query": "What is RAG?"}
	```
	**Response JSON:**
	```json
	{"response": "..."}
	```

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
