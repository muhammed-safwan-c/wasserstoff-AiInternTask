import sys
import pathlib

# Add the backend folder to sys.path
sys.path.append(str(pathlib.Path(__file__).parent.parent / 'backend'))

from app.services.pdf_service import extract_text_from_pdf, is_scanned_pdf

file_path = r"C:\Users\safwa\Downloads\Iam Safwan C .pdf"

print(f"Checking file: {file_path}")

if is_scanned_pdf(file_path):
    print("PDF is scanned (image based)")
else:
    print("PDF is digital (text based)")

text = extract_text_from_pdf(file_path)
print(f"Extracted text length: {len(text)}")
print("Text snippet:", text[:300])
