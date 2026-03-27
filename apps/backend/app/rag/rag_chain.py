"""
RAG chain module for generating responses using retrieved documents and LLM.
"""

import asyncio
import logging

from app.exceptions import RAGPipelineError
from app.rag.retriever import retrieve_docs
from app.services.llm import ask_llm
from app.services.memory import add_to_memory, get_memory

logger = logging.getLogger(__name__)


async def generate_rag_response(query):
    """
    Generate a response using Retrieval-Augmented Generation (RAG).

    Args:
        query (str): The user query.

    Returns:
        tuple: (response from LLM, list of retrieved documents)

    Raises:
        RAGPipelineError: If the RAG pipeline fails.
    """
    try:
        docs = retrieve_docs(query)
        if not docs:
            logger.warning(f"No documents retrieved for query: {query}")

        memory = get_memory()

        memory_text = "\n".join(
            [f"User : {m['query']}\nAssistant: {m['response']}" for m in memory]
        )

        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""
You are an intelligent AI assistant.

Answer the questions using ONLY the provided context.

Guidelines:
- Be clear and structured
- Use bullet points or numbered lists if needed
- If unsure, say you "I don't know"
- Do NOT make up information

Conversation history:
{memory_text}

Context:
{context}

Question:
{query}
"""
        response = await ask_llm(prompt)
        add_to_memory(query, response)
        return response, docs
    except Exception as e:
        logger.error(f"RAG pipeline error: {str(e)}")
        raise RAGPipelineError(f"Failed to generate RAG response: {str(e)}")
