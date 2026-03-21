from app.rag.retriever import retrieve_docs
from app.services.llm import ask_llm

import asyncio

async def generate_rag_response(query):
    docs = retrieve_docs(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an helpful assistant.

Use ONLY the context provided below to answer the question. If you don't know the answer, say you don't know.
Context:
{context}
Question: 
{query}
"""
    response = await ask_llm(prompt)
    return response, docs