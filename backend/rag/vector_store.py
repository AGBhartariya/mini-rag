# from qdrant_client import QdrantClient
# from qdrant_client.http.models import VectorParams, Distance, PointStruct
# import os

# VECTOR_SIZE = 1024
# COLLECTION_NAME = "mini_rag_chunks"


# def get_qdrant_client():
#     return QdrantClient(
#         url=os.getenv("QDRANT_URL"),
#         api_key=os.getenv("QDRANT_API_KEY"),
#     )


# def init_collection():
#     client = get_qdrant_client()

#     collections = client.get_collections().collections
#     if any(c.name == COLLECTION_NAME for c in collections):
#         return

#     client.create_collection(
#         collection_name=COLLECTION_NAME,
#         vectors_config=VectorParams(
#             size=VECTOR_SIZE,
#             distance=Distance.COSINE
#         )
#     )


# def upsert_chunks(vectors, payloads):
#     client = get_qdrant_client()

#     points = [
#         PointStruct(
#             id=payload["chunk_id"],
#             vector=vector,
#             payload=payload
#         )
#         for vector, payload in zip(vectors, payloads)
#     ]

#     client.upsert(
#         collection_name=COLLECTION_NAME,
#         points=points
#     )


# # 🔥 STEP 6: RETRIEVAL FUNCTION
# def search_similar_chunks(query_vector, top_k: int = 5):
#     client = get_qdrant_client()

#     results = client.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=query_vector,
#         limit=top_k,
#         with_payload=True,
#     )

#     return results

# from qdrant_client import QdrantClient
# from qdrant_client.http.models import VectorParams, Distance, PointStruct
# import os
# import uuid

# VECTOR_SIZE = 1024
# COLLECTION_NAME = "mini_rag_chunks"


# def get_qdrant_client():
#     return QdrantClient(
#         url=os.getenv("QDRANT_URL"),
#         api_key=os.getenv("QDRANT_API_KEY"),
#     )


# def init_collection():
#     client = get_qdrant_client()

#     collections = client.get_collections().collections
#     if any(c.name == COLLECTION_NAME for c in collections):
#         return

#     client.create_collection(
#         collection_name=COLLECTION_NAME,
#         vectors_config=VectorParams(
#             size=VECTOR_SIZE,
#             distance=Distance.COSINE,
#         ),
#     )


# def upsert_chunks(vectors, payloads):
#     client = get_qdrant_client()

#     points = []
#     for vector, payload in zip(vectors, payloads):
#         points.append(
#             PointStruct(
#                 id=str(uuid.uuid4()),  # ✅ globally unique
#                 vector=vector,
#                 payload=payload,
#             )
#         )

#     client.upsert(
#         collection_name=COLLECTION_NAME,
#         points=points,
#     )


# def search_similar_chunks(query_vector, top_k: int = 5):
#     client = get_qdrant_client()

#     results = client.search(
#         collection_name=COLLECTION_NAME,
#         query_vector=query_vector,
#         limit=top_k,
#         with_payload=True,
#     )

#     # Normalize results for downstream pipeline
#     chunks = []
#     for r in results:
#         chunks.append({
#             "text": r.payload["text"],
#             "metadata": {
#                 k: v for k, v in r.payload.items() if k != "text"
#             },
#             "score": r.score,
#         })

#     return chunks

# def mmr_select(chunks, lambda_param=0.7, top_k=5):
#     selected = []
#     candidates = chunks.copy()

#     while len(selected) < top_k and candidates:
#         best = None
#         best_score = -1e9

#         for c in candidates:
#             relevance = c["score"]
#             diversity = max(
#                 [abs(c["score"] - s["score"]) for s in selected]
#                 or [0]
#             )

#             score = lambda_param * relevance - (1 - lambda_param) * diversity

#             if score > best_score:
#                 best_score = score
#                 best = c

#         selected.append(best)
#         candidates.remove(best)

#     return selected

from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
import os
import uuid

VECTOR_SIZE = 1024
COLLECTION_NAME = "mini_rag_chunks"


# --------------------------------------------------
# Client
# --------------------------------------------------
def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )


# --------------------------------------------------
# Init collection
# --------------------------------------------------
def init_collection():
    client = get_qdrant_client()

    collections = client.get_collections().collections
    if any(c.name == COLLECTION_NAME for c in collections):
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


# --------------------------------------------------
# Upsert
# --------------------------------------------------
def upsert_chunks(vectors, payloads):
    client = get_qdrant_client()

    points = [
        PointStruct(
            id=str(uuid.uuid4()),   # ✅ unique, avoids overwrite bugs
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
# Search (🔥 NORMALIZED OUTPUT)
# --------------------------------------------------
def search_similar_chunks(query_vector, top_k: int = 5):
    client = get_qdrant_client()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
    )

    # 🔥 Normalize ONCE, here
    return [
        {
            "text": r.payload["text"],
            "metadata": {
                k: v for k, v in r.payload.items() if k != "text"
            },
            "score": r.score,
        }
        for r in results
    ]


# --------------------------------------------------
# MMR Selection
# --------------------------------------------------
def mmr_select(chunks, lambda_param=0.7, top_k=5):
    selected = []
    candidates = chunks.copy()

    while len(selected) < top_k and candidates:
        best = None
        best_score = -1e9

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
