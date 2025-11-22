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
    elapsed = time.time() - start_time
    print(f"Ingestion complete in {elapsed:.2f} seconds.")
    print(f"Chroma DB directory: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
