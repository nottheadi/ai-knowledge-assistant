# API Documentation

This document describes the main API endpoints for the AI Knowledge Assistant.

## Health Check
- `GET /` — Returns API status
  - **Response:**
    ```json
    {"status": "success", "message": "AI Knowledge Assistant API is running."}
    ```

## Chat with AI
- `POST /api/chat`
  - **Request JSON:**
    ```json
    {"query": "What is RAG?"}
    ```
  - **Response JSON:**
    ```json
    {"response": "..."}
    ```

## RAG Chat
- `POST /api/chat/RAG`
  - **Request JSON:**
    ```json
    {"query": "Summarize the uploaded document."}
    ```
    - The request body must be a JSON object with a `query` field (string). Example:
      ```json
      {"query": "What is the summary?"}
      ```

  - **Response JSON:**
    ```json
    {
      "answer": "...",
      "sources": [
        {"page": 1, "source": "document.pdf"},
        {"page": 2, "source": "document.pdf"}
      ]
    }
    ```
  - **Notes:**
    - The RAG response includes a list of sources, each with `page` and `source` fields for traceability.
    - The assistant uses the last 3 chat interactions as context for more relevant answers.

## List Uploaded PDFs
- `GET /api/uploads`
  - **Description:** Returns a list of all uploaded PDF filenames.
  - **Response JSON:**
    ```json
    {"files": ["example1.pdf", "example2.pdf"]}
    ```
  - **Errors:**
    - Returns `{ "error": "..." }` with status 500 if the upload directory cannot be read.

## Upload PDF
- `POST /api/upload`
  - **Form Data:**
    - `file`: PDF file to upload (max 10MB)
  - **Response JSON:**
    ```json
    {"message": "File uploaded and processed successfully."}
    ```
  - **Errors:**
    - Only PDF files are allowed
    - File size exceeds 10MB
    - Invalid PDF signature

## Documentation
- Interactive docs: `/docs` (Swagger UI)
- Redoc: `/redoc`
