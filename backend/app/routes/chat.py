"""
API routes for chat, RAG, and file upload endpoints.
Handles chat with LLM, RAG-based chat, and PDF upload/processing.
"""

import logging
import os
import shutil

from app.rag.pipeline import process_pdf
from app.rag.rag_chain import generate_rag_response
from app.services.llm import ask_llm
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


class ChatRagRequest(BaseModel):
    query: str


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """

    query: str


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    """

    response: str = None
    error: str = None


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat with AI",
    description="Send a query to the AI model and get a response. The model is powered by Google Gemini.",
    responses={200: {"description": "Successful response with AI answer"}},
)
async def chat(request: ChatRequest):
    """
    Chat with the AI model.

    Args:
        request (ChatRequest): The chat request containing the query.

    Returns:
        ChatResponse: The AI's response or error message.
    """
    try:
        logger.info(f"Received chat request: {request.query}")
        response = await ask_llm(request.query)
        logger.info("LLM response generated successfully.")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(error=str(e))


@router.post("/chat/RAG")
async def chat_rag(request: ChatRagRequest):
    """
    Chat with the AI model using Retrieval-Augmented Generation (RAG).

    Args:
        query (str): The user query.

    Returns:
        dict: The AI's answer and source documents, or error message.
    """
    # Input validation
    query = request.query
    if not isinstance(query, str) or not query.strip():
        logger.warning("chat_rag: Query must be a non-empty string.")
        return {"answer": None, "error": "Query must be a non-empty string."}
    try:
        logger.info(f"Received RAG chat request: {query}")
        answer, docs = await generate_rag_response(query)
        sources = [
            {
                "page": doc.metadata.get("page", "N/A"),
                "source": doc.metadata.get("source", "Unknown"),
            }
            for doc in docs
        ]
        logger.info("RAG response generated successfully.")
        return {"answer": answer, "sources": sources}
    except Exception as e:
        logger.error(f"Error in chat_rag endpoint: {e}")
        return {"answer": None, "error": str(e)}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, process it, and store in the vector DB.

    Args:
        file (UploadFile): The uploaded PDF file.

    Returns:
        dict: Success message after processing.
    """
    # Input validation: check file type and extension
    MAX_FILE_SIZE_MB = 10
    if not file.filename.lower().endswith(".pdf"):
        logger.warning(f"upload_pdf: Rejected file upload (not PDF): {file.filename}")
        return {"error": "Only PDF files are allowed."}
    file.file.seek(0, os.SEEK_END)
    file_size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)
    if file_size_mb > MAX_FILE_SIZE_MB:
        logger.warning(
            f"upload_pdf: Rejected file upload (too large): {file.filename}, size: {file_size_mb:.2f} MB"
        )
        return {"error": f"File size exceeds {MAX_FILE_SIZE_MB} MB limit."}
    # Check PDF signature (first 4 bytes should be %PDF)
    header = file.file.read(4)
    file.file.seek(0)
    if header != b"%PDF":
        logger.warning(
            f"upload_pdf: Rejected file upload (invalid PDF signature): {file.filename}"
        )
        return {"error": "Uploaded file is not a valid PDF."}
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File uploaded: {file.filename}")
        # Process the PDF and create vector store
        vectordb = process_pdf(file_path)
        logger.info(f"PDF processed and vector store created for: {file.filename}")
        return {"message": "File uploaded and processed successfully."}
    except Exception as e:
        logger.error(f"Error in upload_pdf endpoint: {e}")
        return {"error": str(e)}


@router.get("/uploads")
async def list_uploaded_pdfs():
    """
    List all uploaded PDF files in the uploads directory.
    Returns:
        dict: List of PDF filenames.
    """
    try:
        files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".pdf")]
        return JSONResponse(content={"files": files})
    except Exception as e:
        logger.error(f"Error listing uploaded PDFs: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
