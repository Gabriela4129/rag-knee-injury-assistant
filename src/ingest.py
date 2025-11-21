import os
import glob
import time
from typing import List

import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

DB_DIR = "data/chroma_db"
COLLECTION_NAME = "knee_guidelines"


def load_text_file(path: str) -> str:
    """
    Load a plain text file as a single string.
    This is much lighter than parsing PDFs and avoids memory issues.
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def simple_chunk_text(
    text: str,
    max_chars: int = 2000,
    overlap: int = 400,
) -> List[str]:
    """
    Simple character-based chunking with overlap.
    Works well for small/medium text files.
    """
    chunks = []
    n = len(text)
    start = 0
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def embed_texts(texts: List[str]) -> List[List[float]]:
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in resp.data]


def build_vector_store():
    os.makedirs(DB_DIR, exist_ok=True)

    db_client = chromadb.PersistentClient(
        path=DB_DIR,
        settings=Settings(allow_reset=True),
    )
    collection = db_client.get_or_create_collection(COLLECTION_NAME)

    # NOTE: now we read ONLY .txt files
    txt_files = glob.glob("data/raw/*.txt")
    print(f"Found {len(txt_files)} text files in data/raw")

    if not txt_files:
        print("No .txt files found. Add some text files to data/raw and run again.")
        return

    doc_id = 0
    for txt_path in txt_files:
        print(f"\nProcessing {txt_path}")
        text = load_text_file(txt_path)
        chunks = simple_chunk_text(text)

        if not chunks:
            print("  Skipped empty file.")
            continue

        ids = []
        metadatas = []
        documents = []

        for i, chunk in enumerate(chunks):
            ids.append(f"doc{doc_id}_chunk{i}")
            metadatas.append(
                {
                    "source": os.path.basename(txt_path),
                    "chunk_index": i,
                }
            )
            documents.append(chunk)

        batch_size = 40
        for start in range(0, len(documents), batch_size):
            batch_docs = documents[start : start + batch_size]
            batch_ids = ids[start : start + batch_size]
            batch_metas = metadatas[start : start + batch_size]

            print(f"  Embedding batch {start}–{start + len(batch_docs)}")
            embeddings = embed_texts(batch_docs)

            collection.add(
                ids=batch_ids,
                documents=batch_docs,
                metadatas=batch_metas,
                embeddings=embeddings,
            )

        doc_id += 1

    print("\nIngestion complete.")


def main():
    t0 = time.time()
    build_vector_store()
    print(f"Done in {time.time() - t0:.2f} seconds")


if __name__ == "__main__":
    main()
