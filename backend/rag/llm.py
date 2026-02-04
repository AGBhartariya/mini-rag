# import os
# from dotenv import load_dotenv
# import cohere

# load_dotenv()

# co = cohere.Client(os.getenv("COHERE_API_KEY"))


# def generate_answer(query: str, contexts: list[str]) -> str:
#     """
#     contexts: list of reranked chunk texts (strings)
#     """

#     if not contexts:
#         return "I don't have enough information to answer this."

#     context_text = "\n\n".join(
#         [f"[{i+1}] {ctx}" for i, ctx in enumerate(contexts)]
#     )

#     system_prompt = """
# You are a factual question-answering system.

# RULES (must follow strictly):
# - Use ONLY the information provided in the sources.
# - Do NOT use any external or prior knowledge.
# - If the question asks for a description, overview, or applications:
#    You MAY synthesize the answer by summarizing information present in the sources.
#    Do NOT introduce facts not present in the sources.
# - Cite the source numbers used.
# - If the sources are truly unrelated, reply:
#     "I don't have enough information to answer this."

# - Cite sources using [1], [2], etc.
# """

#     user_message = f"""
# Sources:
# {context_text}

# Question:
# {query}
# """

#     response = co.chat(
#         model="command-r-08-2024",
#         preamble=system_prompt,
#         message=user_message,
#         temperature=0.1,
#         max_tokens=300,
#     )

#     answer = response.text.strip()

#     # Absolute safety fallback
#     if not answer:
#         return "I don't have enough information to answer this."

#     return answer   # ✅ STRING ONLY


import os
from dotenv import load_dotenv
import cohere
import re

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))


def generate_answer(query: str, contexts: list[str]) -> dict:
    """
    Returns:
    {
        "text": "... answer ... [1][2]",
        "used_indices": [1, 2]
    }
    """

    if not contexts:
        return {
            "text": "I don't have enough information to answer this.",
            "used_indices": []
        }

    context_text = "\n\n".join(
        [f"[{i+1}] {ctx}" for i, ctx in enumerate(contexts)]
    )

    system_prompt = """
You are a factual question-answering system.

RULES:
- Use ONLY the provided sources.
- Do NOT use external knowledge.
- You MAY summarize if the question asks for description or applications strictly from the sources.
- EVERY factual sentence MUST end with at least one citation like [1],[2] etc.
- If you use other sources in the same sentence, you can add multiple citations like [1][2].
- You can list multiple citations as well as multiple sources as well.
- If you cannot cite a sentence, do NOT include it.
- If you use information from a source, you MUST cite it.
- If sources are unrelated, reply exactly:
  "I don't have enough information to answer this."
"""

    user_message = f"""
Sources:
{context_text}

Question:
{query}
"""

    response = co.chat(
        model="command-r-08-2024",
        preamble=system_prompt,
        message=user_message,
        temperature=0.1,
        max_tokens=300,
    )

    answer_text = response.text.strip()

    if not answer_text:
        return {
            "text": "I don't have enough information to answer this.",
            "used_indices": []
        }

    # 🔒 Extract citations like [1], [2]
    used_indices = sorted(
        {int(x) for x in re.findall(r"\[(\d+)\]", answer_text)}
    )

    return {
        "text": answer_text,
        "used_indices": used_indices
    }
