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
  - **Response JSON:**
    ```json
    {"answer": "...", "sources": [ ... ]}
    ```

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
