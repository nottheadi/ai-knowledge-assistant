"""
Configuration for rate limiting and JWT security.
"""

import os
import warnings
from datetime import datetime, timedelta, timezone
from typing import Optional
import jwt
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize rate limiter with default limits
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

# Validate critical environment variables
def validate_env_variables():
    """Validate required environment variables on startup."""

    # Check JWT_SECRET_KEY
    secret = os.getenv("JWT_SECRET_KEY", "")
    if not secret or secret == "your-secret-key-change-in-production":
        warnings.warn(
            "\n" + "="*70 + "\n"
            "⚠️  WARNING: JWT_SECRET_KEY is not set or using default value!\n"
            "This is INSECURE for production use.\n"
            "Set JWT_SECRET_KEY in .env file immediately.\n"
            "="*70,
            UserWarning,
            stacklevel=2
        )

    # Check GOOGLE_API_KEY
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        warnings.warn(
            "GOOGLE_API_KEY environment variable is not set. "
            "LLM operations will fail without it.",
            UserWarning,
            stacklevel=2
        )

# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY") or "your-secret-key-change-in-production"
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))

# Validate on module load
validate_env_variables()

# Security scheme for Bearer token
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token from the Authorization header."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")

        if user_id is None or username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {"user_id": user_id, "username": username}

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
