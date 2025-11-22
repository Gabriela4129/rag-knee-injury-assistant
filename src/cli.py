from rag_pipeline import KneeRAG


def main():
    rag = KneeRAG()
    print("🦵 Knee Injury RAG Assistant (type 'exit' to quit)")
    prompt_versions = {"1": "v1", "2": "v2", "3": "v3"}

    while True:
        print("\nChoose prompt version: 1) zero-shot  2) few-shot structured  3) chain-of-thought")
        pv = input("Enter 1/2/3 (default 1): ").strip() or "1"
        if pv not in prompt_versions:
            print("Invalid choice, defaulting to 1.")
            pv = "1"
        version = prompt_versions[pv]

        question = input("\nYour question: ").strip()
        if question.lower() in {"exit", "quit"}:
            break

        resp = rag.answer(question, prompt_version=version)

        print("\n--- ANSWER ---")
        print(resp.answer)
        print("\n--- METRICS ---")
        print(f"Prompt version: {resp.prompt_version}")
        print(f"Latency: {resp.latency_seconds:.2f} s")
        print(f"Tokens (approx): {resp.token_count}")
        print(f"Estimated cost (hypothetical): ${resp.estimated_cost_usd:.6f}")

        print("\n--- SOURCES ---")
        for i, ch in enumerate(resp.retrieved_chunks, start=1):
            meta = ch.metadata
            print(f"[Source {i}] {meta.get('source')} (page {meta.get('page')})")


if __name__ == "__main__":
    main()
