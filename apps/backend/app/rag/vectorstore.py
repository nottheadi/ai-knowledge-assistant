from app.rag.embedder import get_embeddings
from langchain_community.vectorstores import Chroma

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
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    vectordb.add_documents(chunks)
    vectordb.persist()

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


def delete_from_vector_store(file_path: str) -> int:
    """
    Delete all chunks belonging to a specific file from ChromaDB.

    Args:
        file_path (str): The source path used when the PDF was ingested
                         (e.g. 'uploads/foo.pdf').

    Returns:
        int: Number of chunks deleted.
    """
    embeddings = get_embeddings()
    vectordb = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
    result = vectordb.get(where={"source": file_path})
    ids = result.get("ids", [])
    if ids:
        vectordb.delete(ids=ids)
    return len(ids)
