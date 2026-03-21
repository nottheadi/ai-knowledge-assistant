"""
Text splitter utility for breaking documents into manageable chunks.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(documents):
    """
    Split documents into chunks for embedding and retrieval.

    Args:
        documents (list): List of document objects to split.

    Returns:
        list: List of document chunks.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return splitter.split_documents(documents)
