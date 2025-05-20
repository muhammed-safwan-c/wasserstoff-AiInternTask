# backend/app/api/docs.py
from fastapi import APIRouter
from app.services.db_service import get_all_documents

router = APIRouter()

@router.get("/documents/")
def list_documents():
    return get_all_documents()
