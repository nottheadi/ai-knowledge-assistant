# API Reference

Complete REST API documentation for the AI Knowledge Assistant.

---

## 🔓 Public Endpoints

### Health Check

**GET** `/`

Check if the API is running.

**Response**: `200 OK`
```json
{
  "status": "success",
  "message": "AI Knowledge Assistant API is running."
}
```

---

## 🔐 Authentication Endpoints

### Login

**POST** `/api/auth/login`

Authenticate with username and password to receive a JWT token.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response**: `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors**:
- `401 Unauthorized`: Invalid credentials
- `422 Unprocessable Entity`: Missing/invalid fields

**Example**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "password123"
  }' | jq .
```

---

## 💬 Chat Endpoints

All chat endpoints require JWT authentication.

**Authentication Header**:
```
Authorization: Bearer <access_token>
```

### Direct Chat

**POST** `/api/chat`

Ask a general question without document context. Uses Gemini API directly.

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "What is machine learning?"
}
```

**Query Validation**:
- Minimum length: 1 character
- Maximum length: 5000 characters

**Response**: `200 OK`
```json
{
  "response": "Machine learning is a subset of artificial intelligence..."
}
```

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `422 Unprocessable Entity`: Invalid query length
- `429 Too Many Requests`: Rate limit exceeded (10 req/min)
- `503 Service Unavailable`: LLM API error

**Example**:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Explain quantum entanglement"
  }'
```

### RAG Chat (Document-Aware)

**POST** `/api/chat/RAG`

Query your uploaded documents with AI. Retrieves relevant chunks and generates answers with source attribution.

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "Summarize the document"
}
```

**Query Validation**:
- Minimum length: 1 character
- Maximum length: 5000 characters

**Response**: `200 OK`
```json
{
  "answer": "The document discusses...",
  "sources": [
    {
      "title": "Chapter 1",
      "page": 1,
      "content": "Introduction to the topic..."
    },
    {
      "title": "Chapter 2",
      "page": 3,
      "content": "Key concepts..."
    }
  ]
}
```

**Response Fields**:
- `answer` (string): AI-generated response using document context
- `sources` (array): List of source chunks used to generate the answer
  - `title` (string): Document or section title
  - `page` (number): Page number where chunk was found
  - `content` (string): Chunk text content

**Features**:
- Retrieves top 3 most relevant document chunks
- Includes last 3 chat interactions as context (conversation memory)
- Markdown-formatted responses for better readability
- Source attribution for traceability

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `422 Unprocessable Entity`: Invalid query length
- `429 Too Many Requests`: Rate limit exceeded (10 req/min)
- `500 Internal Server Error`: RAG pipeline error
- `503 Service Unavailable`: LLM API error

**Example**:
```bash
curl -X POST http://localhost:8000/api/chat/RAG \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main topics discussed?"
  }' | jq .answer
```

---

## 📁 File Management Endpoints

All file endpoints require JWT authentication.

### Upload File

**POST** `/api/upload`

Upload a PDF document for processing. File is automatically chunked, embedded, and stored in vector database.

**Request Headers**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body** (Form Data):
- `file` (file, required): PDF document to upload

**File Validation**:
- Type: PDF only
- Maximum size: 10MB
- Invalid PDFs are rejected with 400 error

**Response**: `200 OK`
```json
{
  "message": "File uploaded and processed successfully.",
  "filename": "document.pdf"
}
```

**Processing Details**:
- PDF loaded and text extracted
- Content split into semantic chunks
- Embeddings generated using HuggingFace model
- Vectors stored in ChromaDB for retrieval

**Errors**:
- `400 Bad Request`: Invalid file type or size
- `401 Unauthorized`: Missing or invalid token
- `429 Too Many Requests`: Rate limit exceeded (5 req/min)
- `500 Internal Server Error`: PDF processing failed

**Example**:
```bash
curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

### List Uploaded Files

**GET** `/api/uploads`

Get list of all uploaded PDF files.

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
{
  "files": [
    "document1.pdf",
    "document2.pdf",
    "research_paper.pdf"
  ]
}
```

**Response Fields**:
- `files` (array): List of uploaded filename strings

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `500 Internal Server Error`: Cannot read upload directory

**Example**:
```bash
curl http://localhost:8000/api/uploads \
  -H "Authorization: Bearer YOUR_TOKEN" | jq .files
```

### Delete File

**DELETE** `/api/uploads/{filename}`

Delete an uploaded file and remove it from vector database.

**Path Parameters**:
- `filename` (string, URL-encoded): Name of file to delete

**Request Headers**:
```
Authorization: Bearer <token>
```

**Response**: `200 OK`
```json
{
  "message": "File deleted successfully."
}
```

**Deletion Process**:
- File removed from filesystem
- Embeddings deleted from ChromaDB
- Conversation memory updated

**Errors**:
- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: File does not exist
- `500 Internal Server Error`: Deletion failed

**Example**:
```bash
curl -X DELETE "http://localhost:8000/api/uploads/document.pdf" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## 🔄 Rate Limiting

The API implements rate limiting to prevent abuse:

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/api/chat` | 10 requests | 1 minute |
| `/api/chat/RAG` | 10 requests | 1 minute |
| `/api/upload` | 5 requests | 1 minute |
| Other endpoints | 10 requests | 1 minute (default) |

**Rate Limit Headers**:
```
X-RateLimit-Limit: 10
X-RateLimit-Remaining: 9
X-RateLimit-Reset: 1617234567
```

**Rate Limit Exceeded Response**: `429 Too Many Requests`
```json
{
  "detail": "Rate limit exceeded",
  "error_code": "RATE_LIMIT_EXCEEDED",
  "status_code": 429
}
```

---

## ❌ Error Handling

All endpoints return standardized error responses:

### Error Response Format

```json
{
  "detail": "Error description",
  "error_code": "ERROR_CODE",
  "status_code": 400
}
```

### Common Error Codes

| Status | Code | Reason |
|--------|------|--------|
| 400 | `VALIDATION_ERROR` | Invalid input data |
| 401 | `UNAUTHORIZED` | Missing or invalid token |
| 422 | `VALIDATION_ERROR` | Invalid request fields |
| 429 | `RATE_LIMIT_EXCEEDED` | Too many requests |
| 500 | `INTERNAL_ERROR` | Server error |
| 503 | `LLM_ERROR` | Gemini API unavailable |

### Example Error Response

```json
{
  "detail": "Validation failed",
  "error_code": "VALIDATION_ERROR",
  "status_code": 422,
  "errors": [
    {
      "loc": ["body", "query"],
      "msg": "ensure this value has at most 5000 characters",
      "type": "value_error.str.max_length"
    }
  ]
}
```

---

## 📊 Request/Response Examples

### Complete Login & Chat Flow

```bash
# 1. Login and get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}' \
  | jq -r '.access_token')

echo "Token: $TOKEN"

# 2. Upload a document
curl -X POST http://localhost:8000/api/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@research.pdf"

# 3. List uploaded files
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/uploads

# 4. Query the document
curl -X POST http://localhost:8000/api/chat/RAG \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"Summarize the findings"}' | jq .

# 5. Delete the file
curl -X DELETE "http://localhost:8000/api/uploads/research.pdf" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📖 Interactive Documentation

The API provides interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🔒 Security Notes

- All authenticated endpoints require a valid JWT token in the `Authorization` header
- Tokens expire after 60 minutes (configurable)
- Passwords are hashed with bcrypt
- Tokens are signed with a secret key (set in .env)
- CORS is enabled for development (restrict in production)

---

## 📝 Common Use Cases

### Case 1: Upload Document and Ask Questions

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "username": "admin",
    "password": "password123"
})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Upload document
with open("document.pdf", "rb") as f:
    files = {"file": f}
    requests.post(f"{BASE_URL}/upload", headers=headers, files=files)

# Query document
response = requests.post(f"{BASE_URL}/chat/RAG",
    headers=headers,
    json={"query": "What is the main topic?"}
)
print(response.json()["answer"])
```

### Case 2: Batch Processing

```python
import requests
import time

# Upload multiple documents
documents = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
for doc in documents:
    with open(doc, "rb") as f:
        requests.post(f"{BASE_URL}/upload",
            headers=headers,
            files={"file": f}
        )
    time.sleep(1)  # Rate limiting

# Query with same context
responses = []
for query in ["summary", "key findings", "conclusion"]:
    r = requests.post(f"{BASE_URL}/chat/RAG",
        headers=headers,
        json={"query": query}
    )
    responses.append(r.json())
    time.sleep(1)
```

---

## 🚀 Performance Tips

1. **Reuse JWT Token**: Don't authenticate on every request
2. **Batch Operations**: Upload multiple documents before querying
3. **Caching**: Store responses client-side when appropriate
4. **Async Operations**: Use async/await in your client code
5. **Monitor Rate Limits**: Check `X-RateLimit-*` headers

---

**Last Updated**: March 29, 2026
**API Version**: 1.0.0
**Status**: Stable ✅
