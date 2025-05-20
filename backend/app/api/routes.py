from fastapi import APIRouter
from pydantic import BaseModel
from services.vector_store import query_vectorstore

router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query/")
async def search_documents(request: QueryRequest):
    results = query_vectorstore(request.query)
    # Optional: format results for frontend
    return {
        "results": [
            {
                "text": doc,
                "metadata": meta
            } for doc, meta in zip(results['documents'][0], results['metadatas'][0])
        ]
    }
