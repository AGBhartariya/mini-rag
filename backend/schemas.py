# from pydantic import BaseModel
# from typing import List, Optional, Dict


# class IngestResponse(BaseModel):
#     status: str
#     num_chunks: int
#     embedding_provider: Optional[str] = None



# class IngestRequest(BaseModel):
#     document_text: str
#     title: Optional[str] = "Uploaded Document"


# class AskRequest(BaseModel):
#     query: str


# class Source(BaseModel):
#     id: int
#     text: str
#     metadata: Dict


# class AskResponse(BaseModel):
#     answer: str
#     sources: List[Source]
#     timings: Dict
#     cost_estimate: float

# from pydantic import BaseModel
# from typing import List, Optional, Dict, Any


# class IngestResponse(BaseModel):
#     status: str
#     num_chunks: int
#     embedding_provider: Optional[str] = None


# class IngestRequest(BaseModel):
#     document_text: str
#     title: Optional[str] = "Uploaded Document"


# class AskRequest(BaseModel):
#     query: str


# class Source(BaseModel):
#     id: str              # ✅ UUID is a string
#     text: str
#     metadata: Dict[str, Any]


# # class AskResponse(BaseModel):
# #     answer: str
# #     sources: List[Source]
# #     timings: Dict
# #     cost_estimate: Optional[Dict[str, float]] = None

# class Citation(BaseModel):
#     citation_id: int
#     chunk_id: str


# class AnswerPayload(BaseModel):
#     text: str
#     citations: List[Citation]


# class AskResponse(BaseModel):
#     answer: AnswerPayload
#     sources: List[Source]
#     timings: Dict
#     cost_estimate: Optional[Dict[str, float]] = None


from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class IngestResponse(BaseModel):
    status: str
    num_chunks: int
    embedding_provider: Optional[str] = None


class IngestRequest(BaseModel):
    document_text: str
    title: Optional[str] = "Uploaded Document"


class AskRequest(BaseModel):
    query: str


class Source(BaseModel):
    id: str                  # maps to citation number
    text: str
    metadata: Dict[str, Any]


class Citation(BaseModel):
    citation_id: int         # e.g. 1, 2, 3
    chunk_id: str            # explicit link to source


class AnswerPayload(BaseModel):
    text: str                # answer text with [1], [2]
    citations: List[Citation]


class AskResponse(BaseModel):
    answer: AnswerPayload
    sources: List[Source]
    timings: Dict
    cost_estimate: Optional[Dict[str, float]] = None
