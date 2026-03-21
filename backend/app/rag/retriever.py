from app.rag.vectorstore import load_vector_store

def retrieve_docs(query, k=3):
    vectordb = load_vector_store()

    results = vectordb.similarity_search(query, k=k)
    
    return results