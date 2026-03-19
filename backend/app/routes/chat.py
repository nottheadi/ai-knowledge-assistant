from fastapi import APIRouter
from app.services.llm import ask_llm

router = APIRouter()

@router.post("/chat")
async def chat(query : str):
    response = await ask_llm(query)
    return {"response": response}