from langchain_community.vectorstores import Chroma
from app.rag.embedder import get_embeddings


def create_vectore_store(chunks, embeddings):
    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory="./chroma_db"
    )
    return vectordb

def load_vector_store():
    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory="./chroma_db",embedding_function=embeddings
    )    
    return vectordb
