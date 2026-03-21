"""
RAG chain module for generating responses using retrieved documents and LLM.
"""

from app.rag.retriever import retrieve_docs
from app.services.llm import ask_llm

import asyncio


async def generate_rag_response(query):
    """
    Generate a response using Retrieval-Augmented Generation (RAG).

    Args:
        query (str): The user query.

    Returns:
        tuple: (response from LLM, list of retrieved documents)
    """
    docs = retrieve_docs(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an intelligent AI assistant.

Answer the questions using ONLY the provided context.

Guidelines:
- Be clear and structured
- Use bullet points or numbered lists if needed
- If unsure, say you "I don't know"
- Do NOT make up information

Context:
{context}
Question: 
{query}
"""
    response = await ask_llm(prompt)
    return response, docs
