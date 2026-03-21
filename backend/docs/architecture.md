# Architecture

This document describes the high-level architecture of the AI Knowledge Assistant project.

## Overview
- Modular FastAPI backend
- RAG (Retrieval-Augmented Generation) pipeline
- ChromaDB for vector storage
- Google Gemini API for LLM

## Main Components
- `backend/app/routes/`: API endpoints (`chat`, `RAG chat`, `upload`)
- `backend/app/services/`: LLM service (Google Gemini integration)
- `backend/app/rag/`: RAG pipeline modules:
	- `loader.py`: Loads and parses PDF documents
	- `splitter.py`: Splits documents into chunks
	- `embedder.py`: Generates embeddings using HuggingFace models
	- `vectorstore.py`: Stores and retrieves vectors in ChromaDB
	- `retriever.py`: Retrieves relevant chunks for a query
	- `rag_chain.py`: Orchestrates retrieval and LLM response
- `backend/chroma_db/`: ChromaDB persistent data

## Data Flow
1. User uploads a PDF document via `/api/upload`
2. The document is loaded, split into chunks, embedded, and stored in ChromaDB
3. User queries the API via `/api/chat` or `/api/chat/RAG`
4. For RAG, relevant chunks are retrieved from ChromaDB and sent to the LLM
5. The LLM (Google Gemini) generates an answer using the provided context

## Extensibility
- New document loaders, embedding models, or vector stores can be added by extending the `rag/` modules.
- The API layer is modular and can be expanded for new endpoints or business logic.

Add diagrams or more details as needed.
