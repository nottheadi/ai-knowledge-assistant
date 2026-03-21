from langchain_community.vectorstores import Chroma
from app.rag.embedder import get_embeddings


"""
Vector store utilities for document storage and retrieval using ChromaDB.
"""


def create_vectore_store(chunks, embeddings):
    """
    Create and persist a Chroma vector store from document chunks and embeddings.

    Args:
        chunks (list): List of document chunks.
        embeddings: Embedding function/model.

    Returns:
        Chroma: Persisted vector store instance.
    """
    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory="./chroma_db"
    )
    return vectordb


def load_vector_store():
    """
    Load a persisted Chroma vector store from disk.

    Returns:
        Chroma: Loaded vector store instance.
    """
    embeddings = get_embeddings()

    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    return vectordb
