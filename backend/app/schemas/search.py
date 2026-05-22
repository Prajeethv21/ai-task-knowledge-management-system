from typing import List

from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SearchResult(BaseModel):
    score: float
    text: str
    document_id: int
    chunk_id: int
    document_name: str | None = None
    preview: str | None = None
    uploaded_at: str | None = None


class SearchResponse(BaseModel):
    results: List[SearchResult]
