# Evaluation

This document summarizes quantitative and qualitative evaluation of three prompt versions (`v1`, `v2`, `v3`) tested across **10 clinically-relevant queries**.

Raw results: `results/eval_raw.json`  
Summary metrics: `results/eval_summary.csv`

---

# 1. Setup

- **Model:** Llama 3 (8B) running locally via Ollama  
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`  
- **Vector DB:** Chroma PersistentClient  
- **Documents:** 11 PDFs covering ACL, meniscus, OA, rehab, RTS guidelines  
- **Queries:** 10 questions (diagnosis, imaging, red flags, treatment, RTS)

---

# 2. Quantitative Results

Averages computed from raw JSON.

## **Latency**

| Prompt Version | Avg Total Latency (sec) | Avg LLM Latency (sec) |
|----------------|--------------------------|-------------------------|
| **v1** | ~**77.4 s** | ~**72.6 s** |
| **v2** | ~**102.0 s** | ~**96.7 s** |
| **v3** | ~**61.0 s** | ~**56.0 s** |

**Insights:**
- **v3** is the fastest (surprisingly).  
- **v2** is slowest due to structured format + example prompt.  
- **v1** sits in the middle.

---

## **Token Usage**

| Version | Avg Tokens |
|--------|------------|
| **v1** | ~1550 tokens |
| **v2** | ~1650 tokens |
| **v3** | ~1500 tokens |

**Insights:**
- **v2** uses the most tokens (long structured output).
- **v3** is most efficient.

---

## **Estimated Cost**  
(Using $1 / 1M tokens assumption)

| Version | Cost per Query |
|---------|----------------|
| **v1** | ~$0.00155 |
| **v2** | ~$0.00165 |
| **v3** | ~$0.00150 |

---

# 3. Qualitative Results

### **v1 – Zero-shot**
- Simple and concise  
- Sometimes lacks depth  
- Good first baseline  

### **v2 – Structured**
- Most readable  
- Consistent inclusion of red flags  
- Best for real clinical use  
- Slowest but safest  

### **v3 – Chain of Thought**
- Best reasoning quality  
- Often most accurate  
- Fastest latency  
- Less structured than v2  

---

# 4. Final Recommendation

For clinical quality + readability: **use v2**  
For deep reasoning or expert mode: **use v3**  
v1 should only be used as a fallback or for very simple queries.

---

# 5. Limitations & Future Work

- Latency is high due to running on CPU (local Llama 3).
- Add hybrid retrieval (BM25 + embedding).
- Expand dataset with more OA and MCL/PCL documents.
- Add reranking (e.g. Cross-Encoder).

# Evaluation

This document summarizes quantitative and qualitative evaluation of three prompt versions (`v1`, `v2`, `v3`) tested across **10 clinically-relevant queries**.

Raw results: `results/eval_raw.json`  
Summary metrics: `results/eval_summary.csv`

---

# 1. Setup

- **Model:** Llama 3 (8B) running locally via Ollama  
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`  
- **Vector DB:** Chroma PersistentClient  
- **Documents:** 11 PDFs covering ACL, meniscus, OA, rehab, RTS guidelines  
- **Queries:** 10 questions (diagnosis, imaging, red flags, treatment, RTS)

---

# 2. Quantitative Results

Averages computed from raw JSON.

## **Latency**

| Prompt Version | Avg Total Latency (sec) | Avg LLM Latency (sec) |
|----------------|--------------------------|-------------------------|
| **v1** | ~**77.4 s** | ~**72.6 s** |
| **v2** | ~**102.0 s** | ~**96.7 s** |
| **v3** | ~**61.0 s** | ~**56.0 s** |

**Insights:**
- **v3** is the fastest (surprisingly).  
- **v2** is slowest due to structured format + example prompt.  
- **v1** sits in the middle.

---

## **Token Usage**

| Version | Avg Tokens |
|--------|------------|
| **v1** | ~1550 tokens |
| **v2** | ~1650 tokens |
| **v3** | ~1500 tokens |

**Insights:**
- **v2** uses the most tokens (long structured output).
- **v3** is most efficient.

---

## **Estimated Cost**  
(Using $1 / 1M tokens assumption)

| Version | Cost per Query |
|---------|----------------|
| **v1** | ~$0.00155 |
| **v2** | ~$0.00165 |
| **v3** | ~$0.00150 |

---

# 3. Qualitative Results

### **v1 – Zero-shot**
- Simple and concise  
- Sometimes lacks depth  
- Good first baseline  

### **v2 – Structured**
- Most readable  
- Consistent inclusion of red flags  
- Best for real clinical use  
- Slowest but safest  

### **v3 – Chain of Thought**
- Best reasoning quality  
- Often most accurate  
- Fastest latency  
- Less structured than v2  

---

# 4. Final Recommendation

For clinical quality + readability: **use v2**  
For deep reasoning or expert mode: **use v3**  
v1 should only be used as a fallback or for very simple queries.

---

# 5. Limitations & Future Work

- Latency is high due to running on CPU (local Llama 3).
- Add hybrid retrieval (BM25 + embedding).
- Expand dataset with more OA and MCL/PCL documents.
- Add reranking (e.g. Cross-Encoder).

