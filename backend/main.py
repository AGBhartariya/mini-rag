# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# import time
# from typing import List

# load_dotenv()

# # =========================
# # Schemas
# # =========================
# from schemas import (
#     IngestRequest,
#     IngestResponse,
#     AskRequest,
#     AskResponse,
# )

# # =========================
# # RAG modules
# # =========================
# from rag.chunking import chunk_text
# from rag.embeddings import embed_texts
# from rag.vector_store import (
#     init_collection,
#     upsert_chunks,
#     search_similar_chunks,
# )
# from rag.reranker import rerank
# from rag.llm import generate_answer
# from rag.pdf_loader import extract_text_from_pdf

# # =========================
# # App
# # =========================
# app = FastAPI(title="Mini RAG Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # dev only
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # Utils
# # =========================
# def estimate_tokens(text: str) -> int:
#     """Very rough token estimate (demo-safe)."""
#     return max(1, len(text) // 4)


# def mmr_select(
#     chunks: List[dict],
#     lambda_param: float = 0.7,
#     top_k: int = 8,
# ) -> List[dict]:
#     """
#     Maximal Marginal Relevance (MMR)
#     Expects: {text, metadata, score}
#     """
#     selected = []
#     candidates = chunks.copy()

#     while candidates and len(selected) < top_k:
#         best, best_score = None, -1e9

#         for c in candidates:
#             relevance = c["score"]
#             diversity = max(
#                 [abs(c["score"] - s["score"]) for s in selected] or [0]
#             )

#             score = lambda_param * relevance - (1 - lambda_param) * diversity

#             if score > best_score:
#                 best_score = score
#                 best = c

#         selected.append(best)
#         candidates.remove(best)

#     return selected


# # =========================
# # Health
# # =========================
# @app.get("/health")
# def health():
#     return {"status": "ok"}


# # =========================
# # INGEST (TEXT)
# # =========================
# @app.post("/ingest", response_model=IngestResponse)
# def ingest(req: IngestRequest):
#     try:
#         init_collection()

#         chunks = chunk_text(
#             text=req.document_text,
#             title=req.title,
#             source="user_upload",
#         )

#         if not chunks:
#             raise ValueError("No chunks generated")

#         texts = [c["text"] for c in chunks]
#         embeddings = embed_texts(texts)

#         payloads = [
#             {
#                 "text": c["text"],
#                 "chunk_id": c["chunk_id"],
#                 "title": req.title,
#                 "source": "user_upload",
#                 "start_char": c["start_char"],
#                 "end_char": c["end_char"],
#             }
#             for c in chunks
#         ]

#         upsert_chunks(embeddings, payloads)

#         return {
#             "status": "stored",
#             "num_chunks": len(chunks),
#             "embedding_provider": "cohere",
#         }

#     except Exception as e:
#         print("INGEST ERROR:", repr(e))
#         raise HTTPException(status_code=500, detail=str(e))


# # =========================
# # INGEST (PDF)
# # =========================
# # @app.post("/ingest/pdf", response_model=IngestResponse)
# # async def ingest_pdf(file: UploadFile = File(...)):
# #     try:
# #         if not file.filename.lower().endswith(".pdf"):
# #             raise HTTPException(status_code=400, detail="Only PDF files allowed")

# #         init_collection()

# #         pdf_bytes = await file.read()
# #         extracted_text = extract_text_from_pdf(pdf_bytes)

# #         if not extracted_text.strip():
# #             raise ValueError("No readable text found in PDF")

# #         chunks = chunk_text(
# #             text=extracted_text,
# #             title=file.filename,
# #             source="pdf_upload",
# #         )

# #         texts = [c["text"] for c in chunks]
# #         embeddings = embed_texts(texts)

# #         payloads = [
# #             {
# #                 "text": c["text"],
# #                 "chunk_id": c["chunk_id"],
# #                 "title": file.filename,
# #                 "source": "pdf_upload",
# #                 "start_char": c["start_char"],
# #                 "end_char": c["end_char"],
# #             }
# #             for c in chunks
# #         ]

# #         upsert_chunks(embeddings, payloads)

# #         return {
# #             "status": "stored",
# #             "num_chunks": len(chunks),
# #             "embedding_provider": "cohere",
# #         }

# #     except Exception as e:
# #         print("PDF INGEST ERROR:", repr(e))
# #         raise HTTPException(status_code=500, detail=str(e))

# from fastapi import UploadFile, File
# from rag.pdf_loader import extract_text_from_pdf

# @app.post("/ingest/pdf", response_model=IngestResponse)
# async def ingest_pdf(file: UploadFile = File(...)):
#     try:
#         init_collection()

#         contents = await file.read()
#         text = extract_text_from_pdf(contents)

#         if not text.strip():
#             raise ValueError("No readable text found in PDF")

#         chunks = chunk_text(
#             text=text,
#             title=file.filename,
#             source="pdf_upload",
#         )

#         texts = [c["text"] for c in chunks]
#         embeddings = embed_texts(texts)

#         payloads = [
#             {
#                 "text": c["text"],
#                 "chunk_id": c["chunk_id"],
#                 "title": file.filename,
#                 "source": "pdf",
#                 "start_char": c["start_char"],
#                 "end_char": c["end_char"],
#             }
#             for c in chunks
#         ]

#         upsert_chunks(embeddings, payloads)

#         return {
#             "status": "stored",
#             "num_chunks": len(chunks),
#             "embedding_provider": "cohere",
#         }

#     except Exception as e:
#         print("PDF INGEST ERROR:", repr(e))
#         raise HTTPException(status_code=500, detail=str(e))


# # =========================
# # ASK
# # =========================
# @app.post("/ask", response_model=AskResponse)
# def ask(req: AskRequest):
#     try:
#         # 1. Embed query
#         query_embedding = embed_texts([req.query])[0]

#         # 2. Retrieve from Qdrant (already normalized)
#         t0 = time.time()
#         retrieved = search_similar_chunks(
#             query_vector=query_embedding,
#             top_k=12,
#         )
#         retrieval_ms = int((time.time() - t0) * 1000)

#         if not retrieved:
#             return {
#                 "answer": "I don't have enough information to answer this.",
#                 "sources": [],
#                 "timings": {"retrieval_ms": retrieval_ms, "generation_ms": 0},
#                 "cost_estimate": None,
#             }

#         # 3. MMR selection
#         retrieved = mmr_select(retrieved)

#         # 4. Rerank
#         reranked = rerank(
#             query=req.query,
#             chunks=[
#                 {"text": c["text"], "metadata": c["metadata"]}
#                 for c in retrieved
#             ],
#             top_n=3,
#         )

#         if not reranked:
#             return {
#                 "answer": "I don't have enough information to answer this.",
#                 "sources": [],
#                 "timings": {"retrieval_ms": retrieval_ms, "generation_ms": 0},
#                 "cost_estimate": None,
#             }

#         # 5. Deduplicate
#         seen = set()
#         unique = []
#         for r in reranked:
#             key = r["metadata"].get("chunk_id", r["text"])
#             if key not in seen:
#                 seen.add(key)
#                 unique.append(r)

#         reranked = unique

#         # 6. Generate answer
#         context_texts = [r["text"] for r in reranked]

#         t1 = time.time()
#         answer = generate_answer(req.query, context_texts)
#         generation_ms = int((time.time() - t1) * 1000)

#         # 7. Cost estimate
#         input_tokens = sum(estimate_tokens(t) for t in context_texts)
#         output_tokens = estimate_tokens(answer)

#         cost_estimate = {
#             "input_tokens": input_tokens,
#             "output_tokens": output_tokens,
#             "approx_cost_usd": round((input_tokens + output_tokens) * 0.000002, 6),
#         }

#         # 8. Sources
#         sources = [
#             {
#                 "id": str(i + 1),
#                 "text": r["text"],
#                 "metadata": r["metadata"],
#             }
#             for i, r in enumerate(reranked)
#         ]

#         return {
#             "answer": answer,
#             "sources": sources,
#             "timings": {
#                 "retrieval_ms": retrieval_ms,
#                 "generation_ms": generation_ms,
#             },
#             "cost_estimate": cost_estimate,
#         }

#     except Exception as e:
#         print("ASK ERROR:", repr(e))
#         raise HTTPException(status_code=500, detail=str(e))



# from fastapi import FastAPI, HTTPException, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import load_dotenv
# import time
# from typing import List, Optional, Dict

# load_dotenv()

# # =========================
# # Schemas
# # =========================
# from schemas import (
#     IngestRequest,
#     IngestResponse,
#     AskRequest,
#     AskResponse,
# )

# # =========================
# # RAG modules
# # =========================
# from rag.chunking import chunk_text
# from rag.embeddings import embed_texts
# from rag.vector_store import (
#     init_collection,
#     upsert_chunks,
#     search_similar_chunks,
# )
# from rag.reranker import rerank
# from rag.llm import generate_answer
# from rag.pdf_loader import extract_text_from_pdf

# # =========================
# # App
# # =========================
# app = FastAPI(title="Mini RAG Backend")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # dev only
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # =========================
# # Utils
# # =========================
# def estimate_tokens(text: str) -> int:
#     """Very rough token estimate (demo-safe)."""
#     return max(1, len(text) // 4)


# def mmr_select(
#     chunks: List[dict],
#     lambda_param: float = 0.7,
#     top_k: int = 8,
# ) -> List[dict]:
#     """
#     Maximal Marginal Relevance (MMR)
#     Expects chunks with keys: text, metadata, score
#     """
#     selected = []
#     candidates = chunks.copy()

#     while candidates and len(selected) < top_k:
#         best, best_score = None, -1e9

#         for c in candidates:
#             relevance = c["score"]
#             diversity = max(
#                 [abs(c["score"] - s["score"]) for s in selected] or [0]
#             )
#             score = lambda_param * relevance - (1 - lambda_param) * diversity

#             if score > best_score:
#                 best_score = score
#                 best = c

#         selected.append(best)
#         candidates.remove(best)

#     return selected


# # =========================
# # Health
# # =========================
# @app.get("/health")
# def health():
#     return {"status": "ok"}


# # =========================
# # INGEST (TEXT)
# # =========================
# @app.post("/ingest", response_model=IngestResponse)
# def ingest(req: IngestRequest):
#     try:
#         init_collection()

#         chunks = chunk_text(
#             text=req.document_text,
#             title=req.title,
#             source="user_upload",
#         )

#         if not chunks:
#             raise ValueError("No chunks generated")

#         texts = [c["text"] for c in chunks]
#         embeddings = embed_texts(texts)

#         payloads = [
#             {
#                 "text": c["text"],
#                 "chunk_id": c["chunk_id"],
#                 "title": req.title,
#                 "source": "user_upload",
#                 "start_char": c["start_char"],
#                 "end_char": c["end_char"],
#             }
#             for c in chunks
#         ]

#         upsert_chunks(embeddings, payloads)

#         return {
#             "status": "stored",
#             "num_chunks": len(chunks),
#             "embedding_provider": "cohere",
#         }

#     except Exception as e:
#         print("INGEST ERROR:", repr(e))
#         raise HTTPException(status_code=500, detail=str(e))


# # =========================
# # INGEST (PDF)
# # =========================
# @app.post("/ingest/pdf", response_model=IngestResponse)
# async def ingest_pdf(file: UploadFile = File(...)):
#     try:
#         if not file.filename.lower().endswith(".pdf"):
#             raise HTTPException(status_code=400, detail="Only PDF files allowed")

#         init_collection()

#         contents = await file.read()
#         text = extract_text_from_pdf(contents)

#         if not text.strip():
#             raise ValueError("No readable text found in PDF")

#         chunks = chunk_text(
#             text=text,
#             title=file.filename,
#             source="pdf_upload",
#         )

#         texts = [c["text"] for c in chunks]
#         embeddings = embed_texts(texts)

#         payloads = [
#             {
#                 "text": c["text"],
#                 "chunk_id": c["chunk_id"],
#                 "title": file.filename,
#                 "source": "pdf_upload",
#                 "start_char": c["start_char"],
#                 "end_char": c["end_char"],
#             }
#             for c in chunks
#         ]

#         upsert_chunks(embeddings, payloads)

#         return {
#             "status": "stored",
#             "num_chunks": len(chunks),
#             "embedding_provider": "cohere",
#         }

#     except Exception as e:
#         print("PDF INGEST ERROR:", repr(e))
#         raise HTTPException(status_code=500, detail=str(e))


# # =========================
# # ASK
# # =========================
# @app.post("/ask", response_model=AskResponse)
# def ask(req: AskRequest):
#     try:
#         # --------------------------------------------------
#         # 1. Embed query
#         # --------------------------------------------------
#         query_embedding = embed_texts([req.query])[0]

#         # --------------------------------------------------
#         # 2. Retrieve (normalized dicts)
#         # --------------------------------------------------
#         t0 = time.time()
#         retrieved = search_similar_chunks(
#             query_vector=query_embedding,
#             top_k=12,
#         )
#         retrieval_ms = int((time.time() - t0) * 1000)

#         if not retrieved:
#             return {
#                 "answer": "I don't have enough information to answer this.",
#                 "sources": [],
#                 "timings": {"retrieval_ms": retrieval_ms, "generation_ms": 0},
#                 "cost_estimate": None,
#             }

#         # --------------------------------------------------
#         # 3. MMR selection
#         # --------------------------------------------------
#         retrieved = mmr_select(retrieved)

#         # --------------------------------------------------
#         # 4. Rerank
#         # --------------------------------------------------
#         reranked = rerank(
#             query=req.query,
#             chunks=[
#                 {"text": c["text"], "metadata": c["metadata"]}
#                 for c in retrieved
#             ],
#             top_n=3,
#         )

#         if not reranked:
#             return {
#                 "answer": "I don't have enough information to answer this.",
#                 "sources": [],
#                 "timings": {"retrieval_ms": retrieval_ms, "generation_ms": 0},
#                 "cost_estimate": None,
#             }

#         # --------------------------------------------------
#         # 5. Deduplicate by chunk_id
#         # --------------------------------------------------
#         seen = set()
#         unique = []

#         for r in reranked:
#             key = r["metadata"].get("chunk_id", r["text"])
#             if key not in seen:
#                 seen.add(key)
#                 unique.append(r)

#         reranked = unique

#         # --------------------------------------------------
#         # 6. Generate grounded answer
#         # --------------------------------------------------
#         context_texts = [r["text"] for r in reranked]

#         t1 = time.time()
#         answer = generate_answer(req.query, context_texts)
#         generation_ms = int((time.time() - t1) * 1000)

#         # --------------------------------------------------
#         # 7. Cost estimate
#         # --------------------------------------------------
#         input_tokens = sum(estimate_tokens(t) for t in context_texts)
#         output_tokens = estimate_tokens(answer)

#         cost_estimate = {
#             "input_tokens": input_tokens,
#             "output_tokens": output_tokens,
#             "approx_cost_usd": round((input_tokens + output_tokens) * 0.000002, 6),
#         }

#         # --------------------------------------------------
#         # 8. Explicit source mapping
#         # --------------------------------------------------
#         sources = [
#             {
#                 "id": str(i + 1),            # maps to [1], [2], ...
#                 "text": r["text"],
#                 "metadata": r["metadata"],  # includes chunk_id, title, source
#             }
#             for i, r in enumerate(reranked)
#         ]

#         return {
#             "answer": answer,
#             "sources": sources,
#             "timings": {
#                 "retrieval_ms": retrieval_ms,
#                 "generation_ms": generation_ms,
#             },
#             "cost_estimate": cost_estimate,
#         }

#     except Exception as e:
#         print("ASK ERROR:", repr(e))
#         raise HTTPException(status_code=500, detail=str(e))


from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import time
from typing import List

load_dotenv()

# =========================
# Schemas
# =========================
from schemas import (
    IngestRequest,
    IngestResponse,
    AskRequest,
    AskResponse,
)

# =========================
# RAG modules
# =========================
from rag.chunking import chunk_text
from rag.embeddings import embed_texts
from rag.vector_store import (
    init_collection,
    upsert_chunks,
    search_similar_chunks,
)
from rag.reranker import rerank
from rag.llm import generate_answer
from rag.pdf_loader import extract_text_from_pdf

# =========================
# App
# =========================
app = FastAPI(title="Mini RAG Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Utils
# =========================
def estimate_tokens(text: str) -> int:
    """Rough token estimate (demo-safe)."""
    return max(1, len(text) // 4)


def mmr_select(
    chunks: List[dict],
    lambda_param: float = 0.7,
    top_k: int = 8,
) -> List[dict]:
    """
    Maximal Marginal Relevance (MMR)
    Expects chunks with keys: text, metadata, score
    """
    selected = []
    candidates = chunks.copy()

    while candidates and len(selected) < top_k:
        best, best_score = None, -1e9

        for c in candidates:
            relevance = c["score"]
            diversity = max(
                [abs(c["score"] - s["score"]) for s in selected] or [0]
            )
            score = lambda_param * relevance - (1 - lambda_param) * diversity

            if score > best_score:
                best_score = score
                best = c

        selected.append(best)
        candidates.remove(best)

    return selected


# =========================
# Health
# =========================
@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# INGEST (TEXT)
# =========================
@app.post("/ingest", response_model=IngestResponse)
def ingest(req: IngestRequest):
    try:
        init_collection()

        chunks = chunk_text(
            text=req.document_text,
            title=req.title,
            source="user_upload",
        )

        if not chunks:
            raise ValueError("No chunks generated")

        texts = [c["text"] for c in chunks]
        embeddings = embed_texts(texts)

        payloads = [
            {
                "text": c["text"],
                "chunk_id": c["chunk_id"],
                "title": req.title,
                "source": "user_upload",
                "start_char": c["start_char"],
                "end_char": c["end_char"],
            }
            for c in chunks
        ]

        upsert_chunks(embeddings, payloads)

        return {
            "status": "stored",
            "num_chunks": len(chunks),
            "embedding_provider": "cohere",
        }

    except Exception as e:
        print("INGEST ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# INGEST (PDF)
# =========================
@app.post("/ingest/pdf", response_model=IngestResponse)
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        init_collection()

        pdf_bytes = await file.read()
        text = extract_text_from_pdf(pdf_bytes)

        if not text.strip():
            raise ValueError("No readable text found in PDF")

        chunks = chunk_text(
            text=text,
            title=file.filename,
            source="pdf_upload",
        )

        texts = [c["text"] for c in chunks]
        embeddings = embed_texts(texts)

        payloads = [
            {
                "text": c["text"],
                "chunk_id": c["chunk_id"],
                "title": file.filename,
                "source": "pdf_upload",
                "start_char": c["start_char"],
                "end_char": c["end_char"],
            }
            for c in chunks
        ]

        upsert_chunks(embeddings, payloads)

        return {
            "status": "stored",
            "num_chunks": len(chunks),
            "embedding_provider": "cohere",
        }

    except Exception as e:
        print("PDF INGEST ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))


# =========================
# ASK
# =========================
@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    try:
        # --------------------------------------------------
        # 1. Embed query
        # --------------------------------------------------
        query_embedding = embed_texts([req.query])[0]

        # --------------------------------------------------
        # 2. Retrieve
        # --------------------------------------------------
        t0 = time.time()
        retrieved = search_similar_chunks(
            query_vector=query_embedding,
            top_k=12,
        )
        retrieval_ms = int((time.time() - t0) * 1000)

        if not retrieved:
            return {
                "answer": {
                    "text": "I don't have enough information to answer this.",
                    "citations": [],
                },
                "sources": [],
                "timings": {"retrieval_ms": retrieval_ms, "generation_ms": 0},
                "cost_estimate": None,
            }

        # --------------------------------------------------
        # 3. MMR
        # --------------------------------------------------
        retrieved = mmr_select(retrieved)

        # --------------------------------------------------
        # 4. Rerank
        # --------------------------------------------------
        reranked = rerank(
            query=req.query,
            chunks=[
                {"text": c["text"], "metadata": c["metadata"]}
                for c in retrieved
            ],
            top_n=3,
        )

        if not reranked:
            return {
                "answer": {
                    "text": "I don't have enough information to answer this.",
                    "citations": [],
                },
                "sources": [],
                "timings": {"retrieval_ms": retrieval_ms, "generation_ms": 0},
                "cost_estimate": None,
            }

        # --------------------------------------------------
        # 5. Deduplicate
        # --------------------------------------------------
        seen = set()
        unique = []

        for r in reranked:
            key = r["metadata"].get("chunk_id", r["text"])
            if key not in seen:
                seen.add(key)
                unique.append(r)

        reranked = unique

        # --------------------------------------------------
        # 6. Generate answer (DICT)
        # --------------------------------------------------
        context_texts = [r["text"] for r in reranked]

        t1 = time.time()
        llm_result = generate_answer(req.query, context_texts)
        generation_ms = int((time.time() - t1) * 1000)

        answer_text = llm_result["text"]
        used_indices = llm_result["used_indices"]

        # --------------------------------------------------
        # 7. Explicit citation mapping
        # --------------------------------------------------
        citations = []
        for idx in used_indices:
            if 1 <= idx <= len(reranked):
                citations.append({
                    "citation_id": idx,
                    "chunk_id": str(reranked[idx - 1]["metadata"]["chunk_id"]),
                })

        # --------------------------------------------------
        # 8. Cost estimate
        # --------------------------------------------------
        input_tokens = sum(estimate_tokens(t) for t in context_texts)
        output_tokens = estimate_tokens(answer_text)

        cost_estimate = {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "approx_cost_usd": round((input_tokens + output_tokens) * 0.000002, 6),
        }

        # --------------------------------------------------
        # 9. Sources (FULL list)
        # --------------------------------------------------
        used_set = set(used_indices)
        sources = [
            {
                "id": str(i + 1),
                "text": r["text"],
                "metadata": r["metadata"],
                "used": (i + 1) in used_set,
            }
            for i, r in enumerate(reranked)
        ]

        return {
            "answer": {
                "text": answer_text,
                "citations": citations,
            },
            "sources": sources,
            "timings": {
                "retrieval_ms": retrieval_ms,
                "generation_ms": generation_ms,
            },
            "cost_estimate": cost_estimate,
        }

    except Exception as e:
        print("ASK ERROR:", repr(e))
        raise HTTPException(status_code=500, detail=str(e))
