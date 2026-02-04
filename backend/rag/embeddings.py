import os
from typing import List
from dotenv import load_dotenv
import cohere

# --------------------------------------------------
# Load environment variables FIRST
# --------------------------------------------------
load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise RuntimeError("COHERE_API_KEY not found in environment variables.")

# --------------------------------------------------
# Cohere client
# --------------------------------------------------
co = cohere.Client(COHERE_API_KEY)

# Cohere embed-english-v3.0 → 4096 dims
VECTOR_SIZE = 4096


# --------------------------------------------------
# Embedding function
# --------------------------------------------------
def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using Cohere.

    Returns:
        List of 4096-dim vectors
    """
    if not texts:
        return []

    response = co.embed(
        model="embed-english-v3.0",
        texts=texts,
        input_type="search_document",
    )

    return response.embeddings
