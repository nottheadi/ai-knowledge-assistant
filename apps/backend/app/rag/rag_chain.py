"""
RAG chain module for generating responses using retrieved documents and LLM.
"""

import asyncio

from app.rag.retriever import retrieve_docs
from app.services.llm import ask_llm
from app.services.memory import add_to_memory, get_memory


async def generate_rag_response(query):
    """
    Generate a response using Retrieval-Augmented Generation (RAG).

    Args:
        query (str): The user query.

    Returns:
        tuple: (response from LLM, list of retrieved documents)
    """
    docs = retrieve_docs(query)
    memory = get_memory()

    memory_text = "\n".join(
        [f"User : {m['query']}\nAssistant: {m['response']}" for m in memory]
    )

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an intelligent AI assistant.

Answer the questions using ONLY the provided context. If the user greets you, greet them back. If the user asks how you are, respond with a friendly message. If the user asks for your name, respond with "I am a Knowledge Assistant." For any other questions, use the context to provide accurate and concise answers.

Guidelines:
- Be clear and structured
- Use bullet points or numbered lists if needed
- If unsure, say you "I don't know"
- Do NOT make up information
- Always cite sources from the context when providing answers and if the answer doesen't need a cite, don't cite sources.

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
