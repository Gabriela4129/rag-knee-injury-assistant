"""
Prompt templates for different RAG strategies.
"""

BASE_SYSTEM_PROMPT = """You are an AI assistant specialized in orthopedic knee injuries
(ACL, meniscus, ligaments). Use ONLY the provided context to answer.
If the answer is not in the context, say you don't know and suggest
consulting a medical professional.
"""

def build_prompt_approach_a(context: str, question: str) -> str:
    """Baseline zero-shot prompt."""
    return f"""{BASE_SYSTEM_PROMPT}

Context:
{context}

User question: {question}

Answer:
"""

def build_prompt_approach_b(context: str, question: str) -> str:
    """Few-shot / structured output prompt (to be refined later)."""
    return f"""{BASE_SYSTEM_PROMPT}

You must respond in this structure:
1. Summary
2. Key recommendations
3. Important caveats
4. Sources

Context:
{context}

Question: {question}

Answer in the required structure:
"""

def build_prompt_approach_c(context: str, question: str) -> str:
    """Reasoning-style prompt (short final answer)."""
    return f"""{BASE_SYSTEM_PROMPT}

First, think step by step using only the context. Then provide a short final answer.

Context:
{context}

Question: {question}

Final answer:
"""
