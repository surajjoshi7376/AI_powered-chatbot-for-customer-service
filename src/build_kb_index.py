import os
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

# --------------------------------------------------
# Paths (ABSOLUTE, STREAMLIT SAFE)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
KB_DIR = BASE_DIR / "kb_v2"

# --------------------------------------------------
# Load KB files
# --------------------------------------------------
def load_kb_files(kb_path: Path):
    texts, sources = [], []

    for root, _, files in os.walk(kb_path):
        for fname in files:
            if not fname.endswith(".txt"):
                continue

            fpath = Path(root) / fname
            content = fpath.read_text(encoding="utf-8").strip()

            if len(content) < 50:
                continue

            texts.append(content)
            sources.append(str(fpath.relative_to(kb_path)))

    return texts, sources

# --------------------------------------------------
# Chunking
# --------------------------------------------------
def chunk_text(text, max_words=120, min_chars=40):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) >= min_chars]

    chunks = []
    current = []

    for line in lines:
        words = line.split()

        if len(current) + len(words) <= max_words:
            current.extend(words)
        else:
            chunks.append(" ".join(current))
            current = words

    if current:
        chunks.append(" ".join(current))

    return chunks

# --------------------------------------------------
# Build FAISS Index
# --------------------------------------------------
def build_index():
    # Load embedding model
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Load KB documents
    texts, sources = load_kb_files(KB_DIR)

    if not texts:
        raise ValueError("KB is empty. No documents found.")

    # Chunk documents
    all_chunks, meta = [], []
    for src, text in zip(sources, texts):
        chunks = chunk_text(text)
        for chunk in chunks:
            all_chunks.append(chunk)
            meta.append(src)

    if not all_chunks:
        raise ValueError("No chunks generated from KB.")

    #  EMBED CHUNKS (NOT FULL TEXTS)
    embeddings = model.encode(all_chunks, convert_to_numpy=True)

    # ---- SAFETY CHECKS ----
    if embeddings.ndim != 2:
        raise ValueError(f"Invalid embedding shape: {embeddings.shape}")

    dim = embeddings.shape[1]
    if dim <= 0:
        raise ValueError("Invalid embedding dimension.")

    # Build FAISS index
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    # Debug info
    print(f"[KB] Loaded {len(texts)} documents")
    print(f"[KB] Created {len(all_chunks)} chunks")
    print(f"[KB] Embedding shape: {embeddings.shape}")
    print(f"FAISS index built with {index.ntotal} vectors")

    return index, all_chunks, meta, model
