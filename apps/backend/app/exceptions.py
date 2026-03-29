"""
Custom exceptions and error response models for the API.
"""

from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    detail: str
    error_code: str
    status_code: int


class CustomException(Exception):
    """Base custom exception class."""

    def __init__(
        self,
        message: str,
        error_code: str = "INTERNAL_ERROR",
        status_code: int = 500
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(self.message)


class ValidationError(CustomException):
    """Raised when input validation fails."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400
        )


class LLMError(CustomException):
    """Raised when LLM API call fails."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            status_code=503
        )


class RAGPipelineError(CustomException):
    """Raised when RAG pipeline processing fails."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="RAG_PIPELINE_ERROR",
            status_code=500
        )


class FileUploadError(CustomException):
    """Raised when file upload or processing fails."""

    def __init__(self, message: str):
        super().__init__(
            message=message,
            error_code="FILE_UPLOAD_ERROR",
            status_code=400
        )
