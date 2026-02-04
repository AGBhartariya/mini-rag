# import os
# from typing import List

# import google.generativeai as genai
# from dotenv import load_dotenv

# load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# EMBEDDING_MODEL = "models/embedding-001"
# VECTOR_SIZE = 768


# def embed_texts(texts: List[str]) -> List[List[float]]:
#     """
#     Generate embeddings using Gemini API.
#     """

#     if not os.getenv("GEMINI_API_KEY"):
#         raise RuntimeError("GEMINI_API_KEY not set")

#     embeddings = []
#     for text in texts:
#         result = genai.embed_content(
#             model=EMBEDDING_MODEL,
#             content=text,
#             task_type="retrieval_document"
#         )
#         embeddings.append(result["embedding"])

#     return embeddings

import os
from typing import List

from dotenv import load_dotenv
import cohere

# 🔑 Load environment variables FIRST
load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY not found. Check your .env file.")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

VECTOR_SIZE = 1024  # embed-english-v3.0 output size


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings using Cohere
    """
    response = co.embed(
        model="embed-english-v3.0",
        texts=texts,
        input_type="search_document"
    )
    return response.embeddings
