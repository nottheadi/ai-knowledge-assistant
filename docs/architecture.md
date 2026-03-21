# Architecture

This document describes the high-level architecture of the AI Knowledge Assistant project.

## Overview
- Modular FastAPI backend
- RAG (Retrieval-Augmented Generation) pipeline
- ChromaDB for vector storage
- Google Gemini API for LLM

## Main Components
- `backend/app/routes/`: API endpoints
- `backend/app/services/`: LLM and business logic
- `backend/app/rag/`: RAG pipeline (loader, splitter, embedder, vectorstore)
- `backend/chroma_db/`: ChromaDB data

## Data Flow
1. User uploads document (PDF, etc.)
2. Document is split, embedded, and stored in ChromaDB
3. User queries API
4. Relevant chunks are retrieved and sent to LLM
5. LLM generates answer using context

Add diagrams or more details as needed.
