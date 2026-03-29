"""
LLM service for interacting with Google Gemini models.
Provides async function to query the LLM.
"""

import asyncio
import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

from app.exceptions import LLMError

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

# Configure Gemini API
genai.configure(api_key=API_KEY)


async def ask_llm(prompt):
    """
    Make an async call to the Gemini LLM API.

    Args:
        prompt (str): The prompt/question to send to the LLM.

    Returns:
        str: The LLM's response text.

    Raises:
        LLMError: If the API call fails.
    """
    try:

        def make_request():
            model = genai.GenerativeModel(MODEL)
            response = model.generate_content(prompt)
            return response.text

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, make_request)
        return response
    except Exception as e:
        logger.error(f"Error calling Gemini LLM: {str(e)}")
        raise LLMError(f"Failed to get response from LLM: {str(e)}")
