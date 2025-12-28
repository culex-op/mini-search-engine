from fastapi import APIRouter
from api.models import DocumentIn, SearchQuery, SearchResponse, SearchResult , ChatQuery
from engine.index import InvertedIndex
from engine.search import SearchEngine
from pydantic import BaseModel
from engine.openai import generate_answer
from fastapi import Request



router = APIRouter()

index = InvertedIndex()
search_engine = SearchEngine(index)

@router.post("/chat")
async def chat(request: Request):
    body = await request.json()  
    print("CHAT ENDPOINT HIT", body)

    question = body.get("question")
    top_k = body.get("top_k", 3)

    results = search_engine.search(question, top_k)

    if not results:
        return {"answer": "I could not find relevant documents."}

    context = [index.documents.get(doc_id, "") for doc_id, _ in results]

    answer = generate_answer(question, context)

    return {"answer": answer}

@router.post("/documents")
def add_document(doc: DocumentIn):
    index.add_document(doc.doc_id, doc.text)
    return {"status": "document added"}


@router.post("/search")
def search(query: SearchQuery):
    results = search_engine.search(query.query, query.top_k)

    formatted = []
    for doc_id, score in results:
        formatted.append({
            "doc_id": doc_id,
            "score": score,
            "text": index.documents.get(doc_id, "")
        })

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