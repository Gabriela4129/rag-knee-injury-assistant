# Prompt Engineering

The RAG assistant implements three prompt versions to compare answer quality, structure, and performance.

---

## **V1 – Zero-shot Prompt**
Simple, concise baseline.

**Features:**
- Minimal instructions  
- Short, direct answer  
- Uses citations like `[Source 1]`

**Use cases:**
- Fast Q&A
- Simple factual questions

---

## **V2 – Structured Few-shot Prompt**
Best for clinical clarity and safety.

**Structure enforced:**
- Summary
- Key recommendations (bullets)
- Warnings / red flags
- Source citations

**Advantages:**
- Most readable for clinicians  
- Encourages safety (mentions red flags)  
- Most consistent  

**Disadvantages:**
- Slightly higher latency  
- Longer prompt → more tokens  

**Recommended as default** for clinical use.

---

## **V3 – Chain-of-Thought (Reason → Answer)**
Encourages deep reasoning while keeping final answers short.

**Features:**
- Silent step-by-step reasoning  
- Final answer only (no chain exposed)  
- Good synthesis across documents  

**Advantages:**
- Most accurate for complex questions  
- Fastest latency in your evaluation  
- Lowest token usage  

**Disadvantages:**
- Less structured than V2  

**Best for:** detailed clinical reasoning.

---

# Summary

| Version | Strength | Weakness | Best for |
|--------|----------|----------|----------|
| **v1** | Fast, simple | Least complete | Quick factual Q&A |
| **v2** | Most structured & safe | Slowest | Production use |
| **v3** | Best reasoning & fastest latency | Slightly less structured | Expert mode |
