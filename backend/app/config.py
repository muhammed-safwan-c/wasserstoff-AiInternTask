import os
from pathlib import Path
from pymongo import MongoClient

# Base directory where this file (config.py) resides, going up two levels to reach 'app'
BASE_DIR = Path(__file__).resolve().parent.parent  # Points to: backend/app

# Path to the folder where uploaded files will be saved
UPLOAD_DIR = BASE_DIR / "app" / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Tesseract command path (only for Windows)
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change if needed

# MongoDB config
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["chatbot_theme_db"]
pdf_collection = db["pdf_documents"]

# Local Ollama server URL
# Add this if not present
OLLAMA_URL = "http://localhost:11434"


