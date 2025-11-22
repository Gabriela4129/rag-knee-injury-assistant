# Knee Injury RAG Assistant

A Retrieval-Augmented Generation (RAG) system that assists with knee injury questions (ACL tears, meniscus injuries, rehabilitation, return-to-sport, and knee osteoarthritis).

---

# 🚀 Features
- Local LLM inference via **Ollama (Llama 3)**
- Vector retrieval using **ChromaDB**
- Embeddings via **all-MiniLM-L6-v2**
- Three prompt versions (zero-shot, structured, chain-of-thought)
- Evaluation pipeline (latency, tokens, cost)
- CLI-based assistant with citations

---

# 📁 Project Structure

rag-knee-injury-assistant/ │ ├── data/raw/ # PDF documents (11 clinical sources) ├── chroma_db/ # Local vector store │ ├── src/ │ ├── ingest.py # PDF ingestion + chunking + embeddings │ ├── rag_pipeline.py # Retrieval + LLM + prompts │ ├── cli.py # Interactive assistant │ ├── evaluate.py # Evaluation across 3 prompt versions │ ├── docs/ │ ├── DATA_SOURCES.md │ ├── PROMPTS.md │ ├── EVALUATION.md │ ├── PRODUCTION.md │ ├── .env # Ollama config + chunk settings ├── requirements.txt └── README.md
---

### 🧩 Architecture Diagram

```mermaid
flowchart TD
    A[User CLI] --> B[RAG Pipeline]
    B --> C[ChromaDB Vector Store]
    B --> D[LLM - Llama 3 via Ollama]
    C --> E[Sentence-Transformers Embeddings]
    A -->|query| B
    C -->|retrieved chunks| B
    D -->|final answer| A
---
# ⚙️ Quickstart

### 1. Install dependencies
```bash
pip install -r requirements.txt
2. Ensure Ollama is running
Download Ollama from: https://ollama.com
Start the model:
ollama run llama3
3. Ingest PDFs
Place your clinical PDFs inside:
data/raw/
Run ingestion:
python src/ingest.py
4. Start the CLI assistant
python src/cli.py
5. Run evaluation
python src/evaluate.py
This generates:
* results/eval_raw.json
* results/eval_summary.csv

📚 Dataset
The system uses 11 clinical PDF documents, covering:
* ACL diagnosis & physical tests
* ACL reconstruction rehabilitation
* Return-to-sport protocols
* Meniscus tear pathology & rehabilitation
* Conservative vs surgical ACL treatment
* Knee osteoarthritis evidence-based management
Important: PDFs are not included in the repository due to size and copyright.
To reproduce results, place any 10–15 clinical knee-related PDFs inside:
data/raw/
See docs/DATA_SOURCES.md for document descriptions.

🧠 Prompt Versions
* v1: Zero-shot
* v2: Structured few-shot
* v3: Chain-of-thought
See docs/PROMPTS.md for full templates.

📊 Evaluation
Latency, tokens, and answer quality were measured for 10 clinical queries across all prompt versions.
Includes:
* Total latency
* LLM-only latency
* Token usage
* Cost estimation
* Source citations
See docs/EVALUATION.md for complete results.

🧩 Production Plan
See docs/PRODUCTION.md for:
* API architecture
* Error handling
* Monitoring & logging
* Safety constraints
* Deployment considerations
* Future improvements

✔️ Summary
This project demonstrates a complete end-to-end RAG system:
* Local LLM deployment
* PDF ingestion pipeline
* Embedding & vector search
* Retrieval-augmented generation
* Prompt engineering
* Latency/cost evaluation
* Full documentation (DATA_SOURCES, PROMPTS, EVALUATION, PRODUCTION)
It can be extended into a full clinical-assistant API or UI.
