<<<<<<< HEAD
from pathlib import Path
import os
import uuid
import time

from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from tqdm import tqdm

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "raw"
CHROMA_DIR = BASE_DIR / "chroma_db"

load_dotenv(BASE_DIR / ".env")

CHUNK_SIZE_WORDS = int(os.getenv("CHUNK_SIZE_WORDS", 300))
CHUNK_OVERLAP_WORDS = int(os.getenv("CHUNK_OVERLAP_WORDS", 50))


def chunk_text(text: str, max_words: int, overlap: int):
    words = text.split()
    if not words:
        return []

    chunks = []
    step = max_words - overlap
    for start in range(0, len(words), step):
        end = min(start + max_words, len(words))
        chunk_words = words[start:end]
        if len(chunk_words) < 30:
            # skip tiny chunks
            continue
        chunks.append(" ".join(chunk_words))
        if end == len(words):
            break
    return chunks


def extract_pdf_text(pdf_path: Path):
    reader = PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append((i + 1, text))
    return pages


def get_chroma_client():
    CHROMA_DIR.mkdir(exist_ok=True)
    client = chromadb.Client(
        Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=str(CHROMA_DIR)
        )
    )
    return client


def main():
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Data folder not found: {DATA_DIR}. Create it and add PDFs.")
=======
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
>>>>>>> 58a5aaab77704f39c61b00b958e17de462b8bfc4

    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError(f"No PDFs found in {DATA_DIR}. Add at least one PDF.")

    print(f"Found {len(pdf_files)} PDF files.")

    print("Loading sentence-transformer model...")
    embed_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    client = get_chroma_client()
    collection = client.get_or_create_collection(name="knee_docs")

    all_ids = []
    all_docs = []
    all_metas = []

    start_time = time.time()

    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        doc_name = pdf_path.name
        pages = extract_pdf_text(pdf_path)

        for page_num, page_text in pages:
            chunks = chunk_text(page_text, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS)
            for idx, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                all_ids.append(chunk_id)
                all_docs.append(chunk)
                all_metas.append(
                    {
                        "source": doc_name,
                        "page": page_num,
                        "chunk_index": idx,
                    }
                )

    print(f"Total chunks to embed: {len(all_docs)}")
    if not all_docs:
        print("No chunks produced! Check your PDFs.")
        return

    print("Computing embeddings...")
    embeddings = embed_model.encode(all_docs, convert_to_numpy=True).tolist()

    print("Storing in Chroma...")
    collection.add(
        ids=all_ids,
        documents=all_docs,
        metadatas=all_metas,
        embeddings=embeddings,
    )

    client.persist()
    elapsed = time.time() - start_tim_
