from fastapi import APIRouter, UploadFile, File
import shutil
from app.services.ocr_service import extract_text_from_image
from app.config import UPLOAD_DIR


router = APIRouter()

@router.post("/upload-ocr/")
async def upload_ocr_file(file: UploadFile = File(...)):
    file_path = UPLOAD_DIR / file.filename

    # Save file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text from the saved file
    text = extract_text_from_image(str(file_path))

    return {
        "filename": file.filename,
        "text": text
    }
