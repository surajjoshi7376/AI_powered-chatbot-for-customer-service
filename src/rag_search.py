import numpy as np
import faiss

def search(query, model, index, chunks, sources, k=3):
    q_emb = model.encode([query], normalize_embeddings=True)
    q_emb = q_emb.astype("float32")

    scores, idx = index.search(q_emb, k)

    results = []
    for rank, (score, ix) in enumerate(zip(scores[0], idx[0]), start=1):
        results.append({
            "rank": rank,
            "source": sources[ix],
            "chunk": chunks[ix],
            "score": float(score)
        })
    return results
