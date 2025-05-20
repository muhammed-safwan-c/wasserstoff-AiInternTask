from fastapi import APIRouter, UploadFile, File
import shutil
from app.services.ocr_service import extract_text_from_image
from app.services.theme_detector import detect_theme  # import your detector
from app.config import UPLOAD_DIR

router = APIRouter()

@router.post("/upload-ocr/")
async def upload_ocr_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from image
    text = extract_text_from_image(str(file_path))

    # Detect theme from extracted text
    theme = detect_theme(text)

    return {
        "filename": file.filename,
        "text": text,
        "theme": theme or "Unknown"
    }
