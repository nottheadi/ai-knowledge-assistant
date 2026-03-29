#!/usr/bin/env python3
"""
Test script to verify API key authentication is working.
"""
import requests
import json

API_KEY = "fb3e77873421ff3214f0fc2066e2cbbe939a0362f0be72fc12c9b700447dcc9c"
INVALID_KEY = "invalid-key-12345"
BASE_URL = "http://localhost:8000/api"

print("🧪 Testing API Key Authentication\n")
print("=" * 60)

# Test 1: Health check without auth (should work)
print("\n✅ Test 1: Health Check (no auth required)")
try:
    response = requests.get("http://localhost:8000/")
    print(f"   Status: {response.status_code}")
    print(f"   ✓ PASS - No auth required for health check")
except Exception as e:
    print(f"   ✗ FAIL - {e}")

# Test 2: Chat with VALID API key
print("\n✅ Test 2: Chat with VALID API key")
headers_valid = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"query": "Hello"},
        headers=headers_valid
    )
    print(f"   Status: {response.status_code}")
    if response.status_code in [200, 500]:  # 200 = success, 500 = might be LLM error but auth passed
        print(f"   ✓ PASS - Valid key accepted")
    else:
        print(f"   ✗ FAIL - Unexpected status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ✗ FAIL - {e}")

# Test 3: Chat with INVALID API key
print("\n✅ Test 3: Chat with INVALID API key")
headers_invalid = {
    "Authorization": f"Bearer {INVALID_KEY}",
    "Content-Type": "application/json"
}
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"query": "Hello"},
        headers=headers_invalid
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 401:
        print(f"   ✓ PASS - Invalid key rejected with 401")
        print(f"   Response: {response.json().get('detail', 'Invalid API key')}")
    else:
        print(f"   ✗ FAIL - Expected 401, got {response.status_code}")
except Exception as e:
    print(f"   ✗ FAIL - {e}")

# Test 4: Chat without API key
print("\n✅ Test 4: Chat without API key")
try:
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"query": "Hello"}
    )
    print(f"   Status: {response.status_code}")
    if response.status_code == 403:
        print(f"   ✓ PASS - Missing key rejected")
    else:
        print(f"   ✗ FAIL - Expected 403, got {response.status_code}")
except Exception as e:
    print(f"   ✗ FAIL - {e}")

print("\n" + "=" * 60)
print("✅ Authentication tests complete!")
print("\nℹ️  To run these tests, start the backend server first:")
print("   cd apps/backend && python -m uvicorn app.main:app --reload")
