from app.routes import chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="AI Knowledge Assistant API",
    description="A REST API for querying AI models using Google Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint for readiness probe."""
    return JSONResponse(
        content={
            "status": "success",
            "message": "AI Knowledge Assistant API is running.",
        }
    )


app.include_router(chat.router, tags=["Chat"], prefix="/api")
