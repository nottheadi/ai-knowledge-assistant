from app.config import limiter
from app.exceptions import CustomException, ErrorResponse
from app.routes import chat, auth
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(
    title="AI Knowledge Assistant API",
    description="A REST API for querying AI models using Google Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation failed",
            "error_code": "VALIDATION_ERROR",
            "status_code": 422,
            "errors": exc.errors()
        }
    )


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    """Handle custom application exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.message,
            error_code=exc.error_code,
            status_code=exc.status_code
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="An unexpected error occurred",
            error_code="INTERNAL_ERROR",
            status_code=500
        ).dict()
    )


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    """Handle rate limit exceeded errors."""
    return JSONResponse(
        status_code=429,
        content=ErrorResponse(
            detail="Rate limit exceeded",
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429
        ).dict()
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


app.include_router(auth.router, tags=["Authentication"], prefix="/api")
app.include_router(chat.router, tags=["Chat"], prefix="/api")
