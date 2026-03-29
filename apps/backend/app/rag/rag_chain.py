"""
RAG chain module for generating responses using retrieved documents and LLM.
"""

import asyncio
import logging

from app.exceptions import LLMError, RAGPipelineError
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

        prompt = f"""You are a knowledgeable AI assistant specialized in answering questions using provided documentation.

CORE PRINCIPLES:
1. Answer ONLY using the provided documents
2. Be honest - if docs don't contain the answer, state: "The provided documents don't contain information about this"
3. Do NOT infer, assume, or make up information
4. Structure answers with markdown for clarity

FORMATTING (Frontend parses markdown):
Use:
- ## Subheadings for topics
- **bold** for important terms
- - bullet points for lists
- 1. numbered lists for steps/sequences

CONVERSATION CONTEXT (recent interactions):
{memory_text}

DOCUMENT SOURCES (Top ranked by relevance):
{context}

USER QUESTION:
{query}

RESPONSE (use markdown formatting):"""
        response = await ask_llm(prompt)
        add_to_memory(query, response)
        return response, docs
    except LLMError:
        raise
    except Exception as e:
        logger.error(f"RAG pipeline error: {str(e)}")
        raise RAGPipelineError(f"Failed to generate RAG response: {str(e)}")
