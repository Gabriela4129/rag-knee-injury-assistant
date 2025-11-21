# RAG Knee Injury Assistant

End-to-end Retrieval-Augmented Generation (RAG) demo that answers questions
about orthopedic knee injuries (ACL, meniscus, ligaments) using medical
documents as a knowledge base.

## Project structure

- `src/` – ingestion, RAG pipeline, prompts, and evaluation scripts  
- `data/raw/` – source PDFs (not committed)  
- `data/chroma_db/` – local vector DB (not committed)  
- `docs/` – extra docs (optional)

This is being developed as a learning project and as part of a technical
assignment. The goal is to:

1. Ingest PDF documents into a vector database
2. Implement a simple RAG pipeline using OpenAI + Chroma
3. Compare several prompting strategies
4. Document evaluation and production considerations
