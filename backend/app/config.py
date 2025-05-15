import os
from pathlib import Path

# Path to the folder where uploaded files will be saved
UPLOAD_DIR = Path("app/data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Tesseract command path (only for Windows)
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Change if needed
