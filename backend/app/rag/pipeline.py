from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.embedder import get_embeddings
from app.rag.vectorstore import create_vectore_store

def process_pdf(file_path):
    docs = load_pdf(file_path)
    chunks = split_documents(docs)
    embeddings = get_embeddings()
    vectordb = create_vectore_store(chunks, embeddings)

    return vectordb
