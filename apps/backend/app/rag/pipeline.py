"""
Pipeline for processing PDF files into vector stores for retrieval-augmented generation (RAG).
"""

from app.rag.embedder import get_embeddings
from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectore_store


def process_pdf(file_path):
    """
    Process a PDF file: load, split, embed, and store in vector DB.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        vectordb: The created vector store instance.
    """
    docs = load_pdf(file_path)
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    vectordb = create_vectore_store(chunks, embeddings)

    return vectordb
