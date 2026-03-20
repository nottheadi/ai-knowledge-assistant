import os
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("MODEL")

# Configure Gemini API
genai.configure(api_key=API_KEY)

async def ask_llm(prompt):
    """Make an async call to the Gemini LLM API."""
    try:
        def make_request():
            model = genai.GenerativeModel(MODEL)
            response = model.generate_content(prompt)
            return response.text
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, make_request)
        return response
    except Exception as e:
        raise Exception(f"Error calling Gemini LLM: {str(e)}")