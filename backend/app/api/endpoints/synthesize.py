from fastapi import APIRouter, Query
from app.services.theme_synthesizer import synthesize_themes

router = APIRouter()

@router.get("/synthesize/")
def synthesize_from_documents(q: str = Query(..., description="User query to synthesize themes from")):
    return synthesize_themes(q)
