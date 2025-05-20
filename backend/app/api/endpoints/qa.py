from fastapi import APIRouter, Query
from app.services.qa_service import answer_query

router = APIRouter()

@router.get("/query/")
def query_documents(q: str = Query(..., description="User query string")):
    result = answer_query(q)
    return result
