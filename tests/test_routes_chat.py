import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_chat_endpoint():
    payload = {"query": "Hello, AI!"}
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    assert "response" in response.json() or "error" in response.json()


def test_chat_rag_empty_query():
    response = client.post("/api/chat/RAG", json=None)
    assert response.status_code == 422 or response.json().get("error")


def test_upload_pdf_invalid_type():
    fake_file = io.BytesIO(b"not a pdf")
    response = client.post(
        "/api/upload",
        files={"file": ("test.txt", fake_file, "text/plain")},
    )
    assert response.status_code == 200
    assert response.json()["error"] == "Only PDF files are allowed."


def test_upload_pdf_too_large(monkeypatch):
    class LargeFile:
        def __init__(self):
            self.filename = "large.pdf"
            self._pos = 0

        def seek(self, pos, whence=0):
            self._pos = pos

        def tell(self):
            return 11 * 1024 * 1024  # 11 MB

        def read(self, n=-1):
            return b"%PDF" if n == 4 else b""

        def __getattr__(self, name):
            return lambda *a, **k: None

    file = LargeFile()
    response = client.post(
        "/api/upload",
        files={"file": (file.filename, file, "application/pdf")},
    )
    assert response.status_code == 200
    assert "File size exceeds" in response.json()["error"]
