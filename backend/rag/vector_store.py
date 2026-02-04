import os
import uuid
from typing import List

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct

# --------------------------------------------------
# Config
# --------------------------------------------------
VECTOR_SIZE = 4096  # MUST match Cohere embed-english-v3.0
COLLECTION_NAME = "mini_rag_chunks"


# --------------------------------------------------
# Qdrant client
# --------------------------------------------------
def get_qdrant_client() -> QdrantClient:
    url = os.getenv("QDRANT_URL")
    api_key = os.getenv("QDRANT_API_KEY")

    if not url or not api_key:
        raise RuntimeError("QDRANT_URL or QDRANT_API_KEY missing.")

    return QdrantClient(url=url, api_key=api_key)


# --------------------------------------------------
# Initialize collection (idempotent)
# --------------------------------------------------
def init_collection():
    client = get_qdrant_client()

    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME in existing:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


# --------------------------------------------------
# Upsert chunks
# --------------------------------------------------
def upsert_chunks(vectors: List[List[float]], payloads: List[dict]):
    if not vectors or not payloads:
        return

    client = get_qdrant_client()

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload=payload,
        )
        for vector, payload in zip(vectors, payloads)
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


# --------------------------------------------------
# Search similar chunks (SAFE + NORMALIZED)
# --------------------------------------------------
def search_similar_chunks(query_vector: List[float], top_k: int = 5):
    if not query_vector:
        return []

    client = get_qdrant_client()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )

    normalized = []
    for r in results:
        payload = r.payload or {}
        text = payload.get("text")

        if not text:
            continue

        normalized.append(
            {
                "text": text,
                "metadata": {k: v for k, v in payload.items() if k != "text"},
                "score": r.score,
            }
        )

    return normalized


# --------------------------------------------------
# MMR selection (stable + bounded)
# --------------------------------------------------
def mmr_select(
    chunks: List[dict],
    lambda_param: float = 0.7,
    top_k: int = 5,
):
    """
    Simple score-based MMR.
    Uses similarity scores only (acceptable for demo / eval).
    """

    if not chunks:
        return []

    selected = []
    candidates = chunks.copy()

    while len(selected) < min(top_k, len(chunks)):
        best = None
        best_score = float("-inf")

        for c in candidates:
            relevance = c["score"]

            diversity = max(
                [abs(c["score"] - s["score"]) for s in selected]
                or [0]
            )

            score = lambda_param * relevance - (1 - lambda_param) * diversity

            if score > best_score:
                best_score = score
                best = c

        selected.append(best)
        candidates.remove(best)

    return selected
