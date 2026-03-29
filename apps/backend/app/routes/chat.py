"""
API routes for chat, RAG, and file upload endpoints.
Handles chat with LLM, RAG-based chat, and PDF upload/processing.
"""

import logging
import os
import shutil

from app.config import limiter, verify_jwt_token
from app.exceptions import FileUploadError, ValidationError
from app.rag.pipeline import process_pdf
from app.rag.rag_chain import generate_rag_response
from app.rag.retriever import invalidate_retriever
from app.rag.vectorstore import delete_from_vector_store
from app.services.llm import ask_llm
from fastapi import APIRouter, File, HTTPException, Request, UploadFile, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()


class ChatRagRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=5000,
        description="User query for RAG-based response",
        examples=["What is machine learning?"]
    )


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    """

    query: str = Field(
        min_length=1,
        max_length=5000,
        description="User query for the AI model",
        examples=["What is Python?"]
    )


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
@limiter.limit("10/minute")
async def chat(request: Request, chat_request: ChatRequest, user: dict = Depends(verify_jwt_token)):
    """
    Chat with the AI model.

    Args:
        request (Request): The HTTP request object.
        chat_request (ChatRequest): The chat request containing the query.

    Returns:
        ChatResponse: The AI's response or error message.
    """
    try:
        logger.info(f"Received chat request: {chat_request.query}")
        response = await ask_llm(chat_request.query)
        logger.info("LLM response generated successfully.")
        return ChatResponse(response=response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        # Don't return error in response, let exception handler deal with it
        raise


@router.post("/chat/RAG")
@limiter.limit("10/minute")
async def chat_rag(request: Request, rag_request: ChatRagRequest, user: dict = Depends(verify_jwt_token)):
    """
    Chat with the AI model using Retrieval-Augmented Generation (RAG).

    Args:
        request (Request): The HTTP request object.
        rag_request (ChatRagRequest): The request containing the user query.

    Returns:
        dict: The AI's answer and source documents.
    """
    try:
        query = rag_request.query.strip()
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
        # Don't catch here, let exception handler deal with it
        raise


@router.post("/upload")
@limiter.limit("5/minute")
async def upload_pdf(request: Request, file: UploadFile = File(...), user: dict = Depends(verify_jwt_token)):
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
        raise FileUploadError("Only PDF files are allowed.")

    file.file.seek(0, os.SEEK_END)
    file_size_mb = file.file.tell() / (1024 * 1024)
    file.file.seek(0)
    if file_size_mb > MAX_FILE_SIZE_MB:
        logger.warning(
            f"upload_pdf: Rejected file upload (too large): {file.filename}, size: {file_size_mb:.2f} MB"
        )
        raise FileUploadError(f"File size exceeds {MAX_FILE_SIZE_MB} MB limit.")

    # Check PDF signature (first 4 bytes should be %PDF)
    header = file.file.read(4)
    file.file.seek(0)
    if header != b"%PDF":
        logger.warning(
            f"upload_pdf: Rejected file upload (invalid PDF signature): {file.filename}"
        )
        raise FileUploadError("Uploaded file is not a valid PDF.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    if os.path.isfile(file_path):
        raise FileUploadError(f"'{file.filename}' is already uploaded.")
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File uploaded: {file.filename}")
        # Process the PDF and create vector store
        vectordb = process_pdf(file_path)
        logger.info(f"PDF processed and vector store created for: {file.filename}")
        invalidate_retriever()
        return {"message": "File uploaded and processed successfully."}
    except FileUploadError:
        raise
    except Exception as e:
        logger.error(f"Error in upload_pdf endpoint: {e}")
        if os.path.isfile(file_path):
            os.remove(file_path)
        raise FileUploadError(f"Failed to process PDF: {str(e)}")


@router.get("/uploads")
async def list_uploaded_pdfs(user: dict = Depends(verify_jwt_token)):
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
        raise


@router.delete("/uploads/{filename}")
async def delete_uploaded_pdf(filename: str, user: dict = Depends(verify_jwt_token)):
    """
    Delete an uploaded PDF file by name.
    """
    safe_name = os.path.basename(filename)
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File '{safe_name}' not found.")
    try:
        os.remove(file_path)
        logger.info(f"File deleted from disk: {safe_name}")
        chunks_removed = delete_from_vector_store(file_path)
        logger.info(f"Removed {chunks_removed} chunks from ChromaDB for: {safe_name}")
        invalidate_retriever()
        return {"message": f"'{safe_name}' deleted successfully."}
    except Exception as e:
        logger.error(f"Error deleting file {safe_name}: {e}")
        raise FileUploadError(f"Failed to delete '{safe_name}'.")
