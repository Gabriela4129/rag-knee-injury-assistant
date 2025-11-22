# Production Considerations

## 1. Architecture
A production deployment would use:

- **Backend:** FastAPI service wrapping the RAG pipeline  
- **Vector DB:** Chroma Server or Qdrant  
- **Model hosting:**  
  - Ollama in a GPU container (fast), or  
  - Hosted LLM provider  

## 2. Error Handling
- If no documents retrieved → return “I don’t know based on provided data.”  
- If LLM fails → retry + fallback to shorter prompt  
- If question is out-of-scope → detect via classifier  

## 3. Observability
Log for each request:
- Query  
- Retrieved chunks  
- Latency  
- Prompt version  
- Model tokens  
- Error codes  

## 4. Safety
- Include disclaimers: **not medical advice**  
- Always cite sources  
- Prioritize conservative medical recommendations  

## 5. Optimization Opportunities
- GPU acceleration  
- Smaller quantized models  
- Reranking for retrieval  
- Pre-chunking for faster ingestion  
- Prompt caching  
