"""
Authentication routes for login and logout.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.services.user_service import authenticate_user
from app.config import create_access_token
from datetime import timedelta

router = APIRouter()


class LoginRequest(BaseModel):
    """Login request model."""
    username: str
    password: str


class LoginResponse(BaseModel):
    """Login response model."""
    access_token: str
    token_type: str
    user: dict


@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login endpoint. Returns JWT token on successful authentication.

    Args:
        request: LoginRequest with username and password

    Returns:
        LoginResponse with access_token, token_type, and user info

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Authenticate user
    user = authenticate_user(request.username, request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )

    # Create access token
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": user["id"], "username": user["username"]},
        expires_delta=access_token_expires,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }
