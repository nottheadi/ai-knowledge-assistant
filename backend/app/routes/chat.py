from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import ask_llm

router = APIRouter()

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
    responses={
        200: {"description": "Successful response with AI answer"}
    }
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