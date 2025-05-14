from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
