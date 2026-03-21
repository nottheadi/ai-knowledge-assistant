"""
Embeddings utility for obtaining HuggingFace sentence transformer embeddings.
"""

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embeddings():
    """
    Get HuggingFace sentence transformer embeddings for use in vector store.

    Returns:
        HuggingFaceEmbeddings: Embedding model instance.
    """
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
