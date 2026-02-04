# import os
# from dotenv import load_dotenv
# import cohere

# load_dotenv()

# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# if not COHERE_API_KEY:
#     raise RuntimeError("COHERE_API_KEY not found")

# co = cohere.Client(COHERE_API_KEY)


# def rerank(query: str, chunks: list, top_n: int = 3):
#     """
#     chunks: list of dicts with keys {text, metadata}
#     Returns reranked chunks
#     """

#     documents = [c["text"] for c in chunks]

#     response = co.rerank(
#         model="rerank-v4.0-fast",
#         query=query,
#         documents=documents,
#         top_n=min(top_n, len(documents)),
#     )

#     reranked = []
#     for r in response.results:
#         item = chunks[r.index]
#         item["rerank_score"] = r.relevance_score
#         reranked.append(item)

#     return reranked

import os
from dotenv import load_dotenv
import cohere

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY not found")

co = cohere.Client(COHERE_API_KEY)


def rerank(
    query: str,
    chunks: list,
    top_n: int = 3,
    min_score: float = 0.1,
):
    """
    chunks: list of dicts with keys:
      - text
      - metadata
      - score (optional)

    Returns reranked chunks with rerank_score
    """

    if not chunks:
        return []

    documents = [c["text"] for c in chunks]

    response = co.rerank(
        model="rerank-v4.0-fast",
        query=query,
        documents=documents,
        top_n=min(top_n, len(documents)),
    )

    reranked = []
    for r in response.results:
        if r.relevance_score < min_score:
            continue

        item = chunks[r.index]
        item["rerank_score"] = r.relevance_score
        reranked.append(item)

    return reranked
