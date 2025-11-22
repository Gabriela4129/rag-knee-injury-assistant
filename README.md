# Knee Injury RAG Assistant

A Retrieval-Augmented Generation (RAG) system that assists with knee injury questions (ACL tears, meniscus injuries, rehab, RTS, and OA management).  

---

# Features
- Local LLM inference via *Ollama (Llama 3)*
- Vector retrieval using *ChromaDB*  
- Embeddings via *all-MiniLM-L6-v2*
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

# ⚙️ Quickstart

1. Install dependencies
pip install -r requirements.txt

2. Ensure Ollama is running
Download Ollama from: https://ollama.com

Then start the model:
ollama run llama3

3. Ingest PDFs
Place your clinical PDFs inside:
data/ raw/ 

Then run:
pyton src/inhest.py

4. Start the CLI assisant 
python src/cli.py

5. Run Evaluation
python src/evaluate.py

This generates:
results/eval_raw.json
results/eval_summary.csv
---

# Dataset
The system uses 11 clinical PDF documents, covering:
- ACL diagnosis & physical tests
- ACL reconstruction rehabilitation
- Return-to-sport protocols
- Meniscus tear pathology & rehab
- Conservative vs surgical ACL treatment
- Knee osteoarthritis evidence-based management

Important:
PDFs are not included in the repository due to size and copyright.

To reproduce results, place any 10–15 clinical knee-related PDFs inside data/raw/.

See **docs/DATA_SOURCES.md** for description and documentation used.

---

# Prompt Versions
- **v1:** Zero-shot  
- **v2:** Structured few-shot  
- **v3:** Chain-of-thought  

See **docs/PROMPTS.md** for more details.

---

# Evaluation
Latency, tokens, and answer quality were measured for 10 clinical queries across all prompt versions.
Results include:
- Latency (total + LLM-only)
- Token usage
- Cost estimation
- Answer structure
- Source citations

See **docs/EVALUATION.md** for full results.

---

# Production Plan
See **docs/PRODUCTION.md** file outlines:
- API architecture
- Error handling
- Monitoring & logging
- Safety constraints
- Deployment considerations
- Future improvements.

# Summary
This project demonstrates an end-to-end RAG system:
- Local LLM deployment
- PDF ingestion
- Embedding & vector search
- Prompt engineering
- Latency/cost evaluation
- Documentation such as DATA_SOURCES, PROMPTS, EVALUATION, PRODUCTION

It can be extended into a full clinical-assistant API or UI.
