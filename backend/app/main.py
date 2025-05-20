from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import ocr
from app.api import pdf, docs 
from app.api.endpoints import qa

from app.api.endpoints import synthesize



app = FastAPI(
    title="Document Research & Theme Identifier",
    description="AI Internship Task – Wasserstoff",
    version="1.0.0"
)

# Allow CORS (for frontend integration later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Wasserstoff AI Intern Task Backend is running 🚀"}


app.include_router(ocr.router, prefix="/ocr", tags=["OCR"])


app.include_router(pdf.router, prefix="/pdf", tags=["PDF"])


app.include_router(docs.router)  # ← Register the /documents/ endpoint here


app.include_router(qa.router, tags=["Query & QA"])


app.include_router(synthesize.router, tags=["Theme Synthesis"])
