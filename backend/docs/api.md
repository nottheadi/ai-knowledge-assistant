# API Documentation

This document describes the main API endpoints for the AI Knowledge Assistant.

## Health Check
- `GET /` — Returns API status

## Chat Endpoint
- `POST /chat/` — Query the AI with a question and (optionally) a file
  - Request: JSON with `question` and optional file upload
  - Response: JSON with answer

## Documentation
- Interactive docs: `/docs` (Swagger UI)
- Redoc: `/redoc`

Add more endpoint details and examples as your API grows.
