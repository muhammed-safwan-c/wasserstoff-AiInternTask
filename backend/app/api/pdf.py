from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import aiofiles
from app.config import UPLOAD_DIR
from app.services.pdf_service import extract_text_from_pdf, is_scanned_pdf, extract_text_from_scanned_pdf
from app.services.db_service import store_pdf_data
from app.services.theme_detector import detect_theme
from app.services.vector_store import add_to_vectorstore
import traceback

router = APIRouter()

class PdfUploadResponse(BaseModel):
    filename: str
    source: str
    theme: str
    text_snippet: str

@router.post("/upload-pdf/", response_model=PdfUploadResponse)
async def upload_pdf_file(file: UploadFile = File(...)):
    try:
        print(f"⏳ Receiving file: {file.filename}")
        file_path = UPLOAD_DIR / file.filename

        # Ensure file pointer is at start before reading
        await file.seek(0)

        # Save the uploaded file asynchronously to avoid blocking
        async with aiofiles.open(file_path, "wb") as out_file:
            content = await file.read()  # read file content
            await out_file.write(content)
        print(f"✅ File saved at {file_path}")

        # Detect if scanned or digital pdf
        scanned = is_scanned_pdf(str(file_path))
        print(f"🔍 PDF Type: {'Scanned (Image)' if scanned else 'Digital (Text)'}")

        # Extract text based on PDF type
        if scanned:
            text = extract_text_from_scanned_pdf(str(file_path))
            source = "OCR"
        else:
            text = extract_text_from_pdf(str(file_path))
            source = "Text Extract"

        if not text.strip():
            raise ValueError("❌ Text extraction failed. No content extracted.")

        print(f"📄 Extracted {len(text)} characters from PDF ({source})")

        # Detect theme
        theme = detect_theme(text)
        print(f"🧠 Detected Theme: {theme}")

        # Store in DB
        store_pdf_data(file.filename, text, source, theme)
        print(f"🗃️ Stored in MongoDB: {file.filename}")

        # Add to vector store
        add_to_vectorstore(doc_id=file.filename, text=text, metadata={"theme": theme, "source": source})
        print(f"🧩 Added document chunks to vector store: {file.filename}")

        snippet = text[:300] + ("..." if len(text) > 300 else "")

        return PdfUploadResponse(
            filename=file.filename,
            source=source,
            theme=theme,
            text_snippet=snippet
        )

    except Exception as e:
        print(f"❌ Error during PDF upload:\n{traceback.format_exc()}")
        return PdfUploadResponse(
            filename="",
            source="",
            theme="",
            text_snippet=f"Error: {str(e)}"
        )
