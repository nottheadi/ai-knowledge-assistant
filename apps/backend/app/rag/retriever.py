"""
Retriever utility for fetching relevant documents from the vector store using similarity search.
"""

vectordb = None

from app.rag.vectorstore import load_vector_store


def invalidate_retriever():
    """Force the retriever to reload the vector store on next query."""
    global vectordb
    vectordb = None


def retrieve_docs(query, k=5):
    """
    Retrieve top-k relevant documents from the vector store based on a query.

    Args:
        query (str): The user query for similarity search.
        k (int, optional): Number of top documents to retrieve. Defaults to 5.

    Returns:
        list: List of retrieved document objects.
    """
    global vectordb

    if vectordb is None:
        vectordb = load_vector_store()

    results = vectordb.similarity_search(query, k=k)

    return results
