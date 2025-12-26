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
        {
            "doc_id": doc_id,
            "score": score,
            "text": index.documents.get(doc_id, "")
        }
        for doc_id, score in results
    ]
    return {"results": formatted}


@router.post("/save")
def save_index():
    index.save("index.json")
    return {"status": "index saved"}


@router.post("/load")
def load_index():
    index.load("index.json")
    return {"status": "index loaded"}

@router.get("/documents")
def list_documents():
    return index.documents


@router.get("/documents/{doc_id}")
def get_document(doc_id: int):
    if doc_id not in index.documents:
        return {"error": "document not found"}
    return {
        "doc_id": doc_id,
        "text": index.documents[doc_id]
    }