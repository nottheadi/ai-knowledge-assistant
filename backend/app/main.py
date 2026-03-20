from fastapi import FastAPI
from app.routes import chat

app = FastAPI(
    title="AI Knowledge Assistant API",
    description="A REST API for querying AI models using Google Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(
    chat.router,
    tags=["Chat"],
    prefix="/api"
)