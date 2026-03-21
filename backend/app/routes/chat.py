from fastapi import APIRouter, UploadFile, File
import shutil
import os
from pydantic import BaseModel
from app.services.llm import ask_llm
from app.rag.pipeline import process_pdf

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ChatRequest(BaseModel):
    query: str


class ChatResponse(BaseModel):
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

    - **query**: The question or prompt to send to the AI model

    Returns the AI's response or an error message if the request fails.
    """
    try:
        response = await ask_llm(request.query)
        return ChatResponse(response=response)
    except Exception as e:
        return ChatResponse(error=str(e))


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Process the PDF and create vector store
    vectordb = process_pdf(file_path)

    return {"message": "File uploaded and processed successfully."}
