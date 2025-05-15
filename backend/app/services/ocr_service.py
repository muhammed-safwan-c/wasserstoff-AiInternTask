from PIL import Image
import pytesseract
from app.config import TESSERACT_CMD

# Set tesseract command for Windows
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def extract_text_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text.strip()
