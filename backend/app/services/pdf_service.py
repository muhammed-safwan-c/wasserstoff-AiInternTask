import fitz  # PyMuPDF
from pathlib import Path
from pdf2image import convert_from_path
from app.services.ocr_service import extract_text_from_image
from app.services.vector_store import add_to_vectorstore
import uuid

def extract_text_from_pdf(pdf_path: str, doc_id: str = None) -> str:
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        page_text = page.get_text()
        text += page_text
    doc.close()

    text = text.strip()
    _store_text_to_vector_db(text, pdf_path, doc_id)
    return text


def extract_text_from_scanned_pdf(pdf_path: str, doc_id: str = None) -> str:
    text = ""
    pages = convert_from_path(pdf_path)
    for page in pages:
        temp_path = Path("temp_page.jpg")
        page.save(temp_path, "JPEG")
        text += extract_text_from_image(str(temp_path)) + "\n"
        temp_path.unlink()
    text = text.strip()
    _store_text_to_vector_db(text, pdf_path, doc_id)
    return text


def is_scanned_pdf(pdf_path: str) -> bool:
    doc = fitz.open(pdf_path)
    for page in doc:
        # If any page contains text, it's not scanned
        if page.get_text().strip():
            return False
    return True


def _store_text_to_vector_db(text: str, pdf_path: str, doc_id: str = None):
    if not text.strip():
        print("[VectorDB] No text extracted to store.")
        return

    doc_id = doc_id or str(uuid.uuid4())
    filename = Path(pdf_path).name

    metadata = {
        "filename": filename,
    }

    # Pass whole text to add_to_vectorstore which will chunk + embed internally
    add_to_vectorstore(doc_id=doc_id, text=text, metadata=metadata)

    print(f"[VectorDB] Stored document '{filename}' (doc_id={doc_id})")
