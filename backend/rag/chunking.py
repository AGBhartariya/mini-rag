# from typing import List, Dict


# def chunk_text(
#     text: str,
#     chunk_size: int = 500,
#     overlap: int = 50,
# ) -> List[Dict]:

#     if overlap >= chunk_size:
#         raise ValueError("overlap must be smaller than chunk_size")

#     chunks = []
#     text_length = len(text)
#     start = 0
#     chunk_id = 0

#     while start < text_length:
#         end = min(start + chunk_size, text_length)

#         chunks.append({
#             "chunk_id": chunk_id,
#             "text": text[start:end],
#             "start_char": start,
#             "end_char": end,
#         })

#         chunk_id += 1

#         if end == text_length:
#             break

#         start = end - overlap
#         if start < 0:
#             start = 0

#     return chunks

from typing import List, Dict, Optional


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    *,
    source: str = "Uploaded Document",
    title: Optional[str] = None,
    section: Optional[str] = None,
) -> List[Dict]:
    """
    Chunk text into overlapping segments with metadata.

    Chunk size: 500 characters
    Overlap: 50 characters (~10%)

    Metadata stored per chunk:
    - source
    - title
    - section
    - chunk_id
    - start_char
    - end_char
    """

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    text_length = len(text)
    start = 0
    chunk_id = 0

    while start < text_length:
        end = min(start + chunk_size, text_length)

        chunks.append({
            "chunk_id": chunk_id,
            "text": text[start:end],
            "start_char": start,
            "end_char": end,
            "source": source,
            "title": title,
            "section": section,
        })

        chunk_id += 1

        if end == text_length:
            break

        start = end - overlap
        if start < 0:
            start = 0

    return chunks
