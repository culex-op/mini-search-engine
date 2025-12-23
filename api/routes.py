from fastapi import APIRouter
from api.models import DocumentIn, SearchQuery, SearchResponse, SearchResult
from engine.index import InvertedIndex
from engine.search import SearchEngine

router = APIRouter()

index = InvertedIndex()
search_engine = SearchEngine(index)


@router.post("/documents")
def add_document(doc: DocumentIn):
    index.add_document(doc.doc_id, doc.text)
    return {"status": "document added"}


@router.post("/search", response_model=SearchResponse)
def search(query: SearchQuery):
    results = search_engine.search(query.query, query.top_k)
    formatted = [
        SearchResult(doc_id=doc_id, score=score)
        for doc_id, score in results
    ]
    return SearchResponse(results=formatted)
