"""
Core RAG query pipeline (placeholder version).
"""

def answer_query(question: str, approach: str = "a") -> dict:
    return {
        "answer": "RAG pipeline not implemented yet.",
        "latency": 0.0,
        "total_tokens": 0,
        "approach": approach,
    }


if __name__ == "__main__":
    demo_question = "What is the recommended treatment for a complete ACL tear?"
    resp = answer_query(demo_question, approach="a")
    print(resp["answer"])
