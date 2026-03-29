"""
User service for managing user authentication and credentials.
"""

import json
import os
import bcrypt
from typing import Optional, Dict, Any

USERS_FILE = os.path.join(os.path.dirname(__file__), "../../data/users.json")


def load_users() -> Dict[str, Any]:
    """Load users from JSON file."""
    if not os.path.exists(USERS_FILE):
        return {"users": []}

    with open(USERS_FILE, "r") as f:
        return json.load(f)


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Fetch user by username."""
    users_data = load_users()
    for user in users_data.get("users", []):
        if user["username"] == username:
            return user
    return None


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hashed password."""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False


def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticate user by username and password."""
    user = get_user_by_username(username)
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    # Return user without password
    return {
        "id": user["id"],
        "username": user["username"]
    }
