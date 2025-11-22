# Knee Injury RAG Assistant

A Retrieval-Augmented Generation (RAG) system that assists with knee injury questions (ACL tears, meniscus injuries, rehab, RTS, and OA management).  

---

# Features
- Local LLM inference via **Ollama (Llama 3)*
- Vector retrieval using **ChromaDB*  
- Embeddings via **all-MiniLM-L6-v2*
- Three prompt versions (zero-shot, structured, chain-of-thought)  
- Evaluation pipeline (latency, tokens, cost)  
- CLI-based assistant with citations

---

# Project Structure
rag-knee-injury-assistant/
│
├── data/raw/ # PDF documents (11 clinical sources)
├── chroma_db/ # Local vector store
├── src/
│ ├── ingest.py # PDF ingestion + chunking + embeddings
│ ├── rag_pipeline.py # Retrieval + LLM + prompts
│ ├── cli.py # Interactive assistant
│ ├── evaluate.py # Evaluation across 3 prompt versions
│
├── docs/
│ ├── DATA_SOURCES.md
│ ├── PROMPTS.md
│ ├── EVALUATION.md
│ ├── PRODUCTION.md
│
├── .env # Ollama config + chunk settings
├── requirements.txt
├── README.md



---

# Quickstart

### 1. Install dependencies
pip isntall -r requirements.txt

### 2. Run Ollama
ollama run llama 3

# 3. Ingest PDFs
pyton src/inhest.py

# 4. Start the assisant 
python src/evaluate.py


---

# Dataset
The system uses **11 documents** covering:

- ACL diagnosis  
- ACL reconstruction rehab  
- Return-to-sport criteria  
- Meniscus tears  
- Meniscus rehab  
- ACL conservative vs surgical treatment  
- Knee osteoarthritis management  

Note: The PDFs used for ingestion are not included in the repository due to size and copyright.
To reproduce results, place any 10–15 clinical knee-related PDFs inside data/raw/.

See **docs/DATA_SOURCES.md**.

---

# Prompt Versions
- **v1:** Zero-shot  
- **v2:** Structured few-shot  
- **v3:** Chain-of-thought  

See **docs/PROMPTS.md**.

---

# Evaluation
Latency, tokens, accuracy, and cost measured across all prompts with real data.  

See **docs/EVALUATION.md**.

---

# Production Plan
See **docs/PRODUCTION.md**.


