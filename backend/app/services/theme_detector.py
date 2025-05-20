import requests
from app.config import OLLAMA_URL

def detect_theme(text: str) -> str:
    try:
        prompt = f"""
You are a document classifier. Read the content and decide the document type. Choose one of:
["Resume", "Certificate", "Invoice", "Report", "Research Paper", "Unknown"].

Document content:
{text}

Type:
"""
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3",  # Change this to your model name
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            return response.json().get("response", "Unknown").strip()
        else:
            print("Ollama Error:", response.status_code, response.text)
            return "Unknown"

    except Exception as e:
        print("Theme Detection Error:", str(e))
        return "Unknown"
