#!/usr/bin/env python3
"""Test script to verify JWT authentication endpoints."""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_login():
    """Test login endpoint."""
    print("=" * 50)
    print("Testing Login Endpoint")
    print("=" * 50)

    payload = {
        "username": "admin",
        "password": "password123"
    }

    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        return response.json()["access_token"]
    return None


def test_chat_without_token():
    """Test chat endpoint without token (should fail)."""
    print("\n" + "=" * 50)
    print("Testing Chat Without Token (Expected to fail)")
    print("=" * 50)

    payload = {"query": "Hello"}
    response = requests.post(f"{BASE_URL}/api/chat", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_chat_with_token(token):
    """Test chat endpoint with valid token."""
    print("\n" + "=" * 50)
    print("Testing Chat With Token (Expected to succeed)")
    print("=" * 50)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {"query": "What is machine learning?"}
    response = requests.post(f"{BASE_URL}/api/chat", json=payload, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {json.dumps(response.json(), indent=2)}")


def test_invalid_login():
    """Test login with incorrect credentials."""
    print("\n" + "=" * 50)
    print("Testing Login With Invalid Credentials")
    print("=" * 50)

    payload = {
        "username": "admin",
        "password": "wrongpassword"
    }

    response = requests.post(f"{BASE_URL}/api/auth/login", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    try:
        # Test invalid login
        test_invalid_login()

        # Test login
        token = test_login()

        # Test chat without token
        test_chat_without_token()

        # Test chat with token
        if token:
            test_chat_with_token(token)

        print("\n" + "=" * 50)
        print("✓ All tests completed!")
        print("=" * 50)

    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the backend server.")
        print("Make sure the backend is running on http://localhost:8000")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

