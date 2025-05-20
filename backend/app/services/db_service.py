from datetime import datetime
from pymongo import MongoClient
from app.config import pdf_collection, MONGO_URI

# ✅ Store PDF Data with theme
def store_pdf_data(file_name: str, text: str, source: str, theme: str):
    document = {
        "file_name": file_name,
        "text_content": text,
        "source": source,
        "theme": theme,
        "timestamp": datetime.utcnow()
    }
    pdf_collection.insert_one(document)

# ✅ MongoDB Setup for retrieval
client = MongoClient(MONGO_URI)
db = client["chatbot_theme_db"]
collection = db["pdf_documents"]

# ✅ Get All Documents
def get_all_documents():
    docs = collection.find({}, {"_id": 0, "file_name": 1, "source": 1, "text_content": 1, "theme": 1})
    results = [
        {
            "filename": doc.get("file_name", "Unknown"),
            "source": doc.get("source", "Unknown"),
            "content": doc.get("text_content", ""),
            "theme": doc.get("theme", "Unknown")
        }
        for doc in docs
    ]
    return results
