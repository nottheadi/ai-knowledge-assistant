from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm import ask_llm

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
async def chat(request: ChatRequest):
    """Handle chat requests and return LLM responses."""
    try:
        response = await ask_llm(request.query)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}