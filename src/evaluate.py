import time
from pathlib import Path
import json

import pandas as pd

from rag_pipeline import KneeRAG

BASE_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = BASE_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)

TEST_QUERIES = [
    "What are the typical symptoms of an ACL tear compared to a meniscus tear?",
    "When is MRI indicated for suspected knee ligament injury?",
    "What are the main non-surgical treatments for knee osteoarthritis?",
    "Which red-flag symptoms in knee pain require urgent referral?",
    "What are the return-to-sport criteria after ACL reconstruction?",
    "How long is typical rehabilitation after ACL surgery?",
    "When should a patient with knee pain avoid high-impact sports?",
    "What conservative treatments are recommended for partial ACL tears?",
    "How does age influence treatment choice for ACL injuries?",
    "What complications should clinicians monitor after knee surgery?",
]

PROMPT_VERSIONS = ["v1", "v2", "v3"]

def run_evaluation():
    rag = KneeRAG()
    rows = []

    for pv in PROMPT_VERSIONS:
        print(f"\n=== Evaluating prompt version: {pv} ===")
        for q in TEST_QUERIES:
            print(f"- Query: {q}")
            start = time.time()
            resp = rag.answer(q, prompt_version=pv)
            total_time = time.time() - start

            rows.append(
                {
                    "prompt_version": pv,
                    "question": q,
                    "answer": resp.answer,
                    "latency_model_only_sec": resp.latency_seconds,
                    "latency_total_sec": total_time,
                    "token_count": resp.token_count,
                    "estimated_cost_usd": resp.estimated_cost_usd,
                    "num_sources": len(resp.retrieved_chunks),
                    "sources": [
                        {
                            "source": ch.metadata.get("source"),
                            "page": ch.metadata.get("page"),
                        }
                        for ch in resp.retrieved_chunks
                    ],
                }
            )

    # Save detailed JSON
    json_path = RESULTS_DIR / "eval_raw.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)

    # Summary metrics by prompt_version
    df = pd.DataFrame(rows)
    summary = (
        df.groupby("prompt_version")[["latency_total_sec", "token_count", "estimated_cost_usd"]]
        .mean()
        .reset_index()
    )
    csv_path = RESULTS_DIR / "eval_summary.csv"
    summary.to_csv(csv_path, index=False)

    print(f"\nSaved raw results to: {json_path}")
    print(f"Saved summary metrics to: {csv_path}")
    print("\nNow you can manually score correctness/completeness in eval_raw.json and describe in EVALUATION.md.")

if __name__ == "__main__":
    run_evaluation()
