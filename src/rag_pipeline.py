import os
import time
from dataclasses import dataclass
from typing import List, Dict, Any
from pathlib import Path

from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests

BASE_DIR = Path(__file__).resolve().parents[1]
CHROMA_DIR = BASE_DIR / "chroma_db"

load_dotenv(BASE_DIR / ".env")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
TOP_K_DEFAULT = int(os.getenv("TOP_K", 4))

DOLLAR_PER_1M_TOKENS = float(os.getenv("DOLLAR_PER_1M_TOKENS", 1.0))


@dataclass
class RetrievedChunk:
    text: str
    metadata: Dict[str, Any]


@dataclass
class RAGResponse:
    answer: str
    latency_seconds: float
    token_count: int
    estimated_cost_usd: float
    retrieved_chunks: List[RetrievedChunk]
    prompt_version: str


def get_chroma_client():
    client = chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(CHROMA_DIR)
        )
    )
    return client


class KneeRAG:
    def __init__(self):
        self.embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.client = get_chroma_client()
        self.collection = self.client.get_or_create_collection(name="knee_docs")

    def retrieve(self, query: str, top_k: int = TOP_K_DEFAULT) -> List[RetrievedChunk]:
        query_emb = self.embed_model.encode(query, convert_to_numpy=True).tolist()
        res = self.collection.query(
            query_embeddings=[query_emb],
            n_results=top_k,
        )
        docs = res["documents"][0]
        metas = res["metadatas"][0]

        chunks = [
            RetrievedChunk(text=doc, metadata=meta) for doc, meta in zip(docs, metas)
        ]
        return chunks

    def _build_context_str(self, chunks: List[RetrievedChunk]) -> str:
        parts = []
        for i, ch in enumerate(chunks):
            src = ch.metadata.get("source", "unknown")
            page = ch.metadata.get("page", "?")
            parts.append(
                f"[Source {i+1} | {src} | page {page}]\n{ch.text}"
            )
        return "\n\n---\n\n".join(parts)

    # ---------- PROMPTS ----------

    def build_prompt_v1_zero_shot(self, question: str, chunks: List[RetrievedChunk]) -> str:
        context = self._build_context_str(chunks)
        return f"""You are an AI assistant helping clinicians with knee injuries (ACL tears, meniscus injuries, osteoarthritis, etc.).
Answer ONLY based on the context below. If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}

Answer in one or two concise paragraphs and cite sources like [Source 1], [Source 2]."""

    def build_prompt_v2_few_shot_structured(self, question: str, chunks: List[RetrievedChunk]) -> str:
        context = self._build_context_str(chunks)
        example = """Example:
Question: What are the main non-surgical treatments for knee osteoarthritis in young athletes?
Answer:
- Summary: Non-surgical management focuses on pain control, load management, and muscle strengthening.
- Key recommendations:
  1) Activity modification and weight management.
  2) Physiotherapy with quadriceps and hip strengthening.
  3) NSAIDs or acetaminophen as first-line pharmacologic options.
- Warnings / red flags: Persistent swelling, locking, or instability requiring specialist assessment.
Sources: [Source 1], [Source 3]
"""

        return f"""You are a knee-injury clinical assistant.
Use ONLY the context to answer the question. If missing info, clearly state that.

Context:
{context}

{example}

Now answer the user question in the same structure.

Question: {question}

Answer format:
- Summary: ...
- Key recommendations: (bullet list)
- Warnings / red flags: ...
Sources: [Source X], [Source Y]"""

    def build_prompt_v3_chain_of_thought(self, question: str, chunks: List[RetrievedChunk]) -> str:
        context = self._build_context_str(chunks)
        return f"""You are an experienced sports medicine specialist focusing on knee injuries.

TASK:
1) Think step by step about the question and the context.
2) First, silently reason and compare the evidence in the context.
3) Then provide a short final answer (without showing your step-by-step reasoning).
4) If the context is insufficient, say you don't know and suggest what information is missing.

Context:
{context}

Question: {question}

Final answer (no step-by-step reasoning, just conclusions with citations like [Source 2]):"""

    # ---------- LLM CALL ----------

    def _call_ollama(self, prompt: str, temperature: float = 0.2):
        url = f"{OLLAMA_URL.rstrip('/')}/api/generate"
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature
            }
        }

        t0 = time.time()
        resp = requests.post(url, json=payload, timeout=180)
        latency = time.time() - t0

        resp.raise_for_status()
        data = resp.json()
        text = data.get("response", "")
        token_count = int(data.get("eval_count", 0)) + int(data.get("prompt_eval_count", 0))

        cost = (token_count / 1_000_000) * DOLLAR_PER_1M_TOKENS

        return text.strip(), latency, token_count, cost

    def answer(self, question: str, prompt_version: str = "v1", top_k: int = TOP_K_DEFAULT) -> RAGResponse:
        chunks = self.retrieve(question, top_k=top_k)

        if prompt_version == "v1":
            prompt = self.build_prompt_v1_zero_shot(question, chunks)
        elif prompt_version == "v2":
            prompt = self.build_prompt_v2_few_shot_structured(question, chunks)
        elif prompt_version == "v3":
            prompt = self.build_prompt_v3_chain_of_thought(question, chunks)
        else:
            raise ValueError(f"Unknown prompt_version: {prompt_version}")

        answer, latency, tokens, cost = self._call_ollama(prompt)

        return RAGResponse(
            answer=answer,
            latency_seconds=latency,
            token_count=tokens,
            estimated_cost_usd=cost,
            retrieved_chunks=chunks,
            prompt_version=prompt_version,
        )
