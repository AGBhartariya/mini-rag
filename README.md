# Mini RAG System : Retrieval, Reranking & Grounded Citations

This project is a full-stack **Retrieval-Augmented Generation (RAG)** system that ingests documents (text or PDF), retrieves relevant chunks using vector search, reranks them for diversity and relevance, and generates **grounded answers with explicit citations**.

The goal of this project is to demonstrate a **correct, inspectable, and evaluable RAG pipeline**, rather than a black-box chatbot.

---

## 🔗 Live URLs

- **Frontend (Vercel):** https://mini-rag-73lp.vercel.app/
- **Backend (Render):** https://mini-rag-f1l0.onrender.com
- **Backend Health Check:** https://mini-rag-f1l0.onrender.com/health

---

## 📂 Public GitHub Repository

- **Repo:** https://github.com/AGBhartariya/mini-rag

---

## 👤 Author

**Abhigyan Gopal Bhartariya**  
- **Resume:** https://drive.google.com/file/d/1fm0_bcoCFBMJHN_7Y5qhN1a1EOVA3Plp/view?usp=drive_link  
- **GitHub:** https://github.com/AGBhartariya  
- **LinkedIn:** https://www.linkedin.com/in/abhigyan-bhartariya-73267928a/

---

## 🧠 What This System Does

1. Accepts **raw text or PDF uploads**
2. Splits documents into overlapping semantic chunks
3. Generates embeddings using **Cohere**
4. Stores vectors in **Qdrant**
5. Retrieves relevant chunks for a user query
6. Applies **MMR (Maximal Marginal Relevance)** to improve diversity
7. Reranks chunks for relevance
8. Generates answers **strictly from retrieved sources**
9. Appends **inline citations** like `[1]`, `[2]`
10. Maps citations to exact source chunks in the UI

This ensures **traceability, grounding, and evaluation-readiness**.

---

## 🏗️ Architecture Overview

```text
Frontend (Next.js)
   |
   |  REST API
   v
Backend (FastAPI)
   |
   |-- Chunking
   |-- Embedding (Cohere)
   |-- Vector Storage (Qdrant)
   |-- Retrieval
   |-- MMR Selection
   |-- Reranking
   |-- LLM Answer Generation (with citations)
   |
Vector Database (Qdrant Cloud)


---
## 🧩 Tech Stack

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS

### Backend
- Python
- FastAPI
- Cohere SDK
- Qdrant Client

### Models & Services
- **Embeddings:** `embed-english-v3.0`
- **LLM:** `command-r-08-2024`
- **Vector DB:** Qdrant Cloud
```
---

## 📐 Schema & Index Configuration

This project uses **Qdrant** as the vector database to store document chunks and perform semantic retrieval.

### Vector Collection

- **Collection name:** `mini_rag_chunks`
- **Vector size:** `4096`
- **Distance metric:** `Cosine similarity`
- **Embedding model:** `Cohere embed-english-v3.0`

The vector size is aligned with the output dimension of the selected Cohere embedding model.

---

### Stored Payload Schema

Each embedded document chunk is stored with the following payload:

```json
{
  "text": "string (chunk text)",
  "chunk_id": "string",
  "source": "string (document name / file)",
  "page": "number | null",
  "start_char": "number | null",
  "end_char": "number | null"
}

