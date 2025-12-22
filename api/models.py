from pydantic import BaseModel
from typing import List


class DocumentIn(BaseModel):
    doc_id: int
    text: str


class SearchQuery(BaseModel):
    query: str
    top_k: int = 10


class SearchResult(BaseModel):
    doc_id: int
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
