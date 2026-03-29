"""
Configuration for rate limiting and API security.
"""

import os
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Initialize rate limiter with default limits
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

# API Key configuration
API_KEY = os.getenv("API_KEY", "default-dev-key")

# Security scheme for API key
security = HTTPBearer()


async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify the API key from the Authorization header."""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
