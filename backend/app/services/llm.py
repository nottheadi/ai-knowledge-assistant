import os
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL")
MODEL = os.getenv("MODEL")

async def ask_llm(prompt):
    """Make an async call to the LLM API."""
    try:
        def make_request():
            return requests.post(
                f"{BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, make_request)
        response.raise_for_status()
        
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise Exception(f"Unexpected response format: {str(e)}")
    except Exception as e:
        raise Exception(f"Error calling LLM: {str(e)}")