
"""
API routes for chat, RAG, and file upload endpoints.
Handles chat with LLM, RAG-based chat, and PDF upload/processing.
"""

from fastapi import APIRouter, UploadFile, File
import shutil
import os
from pydantic import BaseModel
from app.services.llm import ask_llm
from app.rag.pipeline import process_pdf
from app.rag.rag_chain import generate_rag_response

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



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
        response = await ask_llm(request.query)
        return ChatResponse(response=response)
    except Exception as e:
        return ChatResponse(error=str(e))

@router.post("/chat/RAG")
async def chat_rag(query):
    """
    Chat with the AI model using Retrieval-Augmented Generation (RAG).

    Args:
        query (str): The user query.

    Returns:
        dict: The AI's answer and source documents, or error message.
    """
    try:
        answer, docs = await generate_rag_response(query)
        sources = [doc.metadata.get("source", "Unknown") for doc in docs]
        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
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
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the PDF and create vector store
    vectordb = process_pdf(file_path)

    return {"message": "File uploaded and processed successfully."}
