Document Research & Theme Identification Chatbot
AI Internship Task for Wasserstoff - A chatbot that can process 75+ documents, identify themes, and answer queries with citations.

Project Structure
chatbot_theme_identifier/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── qa.py
│   │   │   │   └── synthesize.py
│   │   │   ├── __init__.py
│   │   │   ├── docs.py
│   │   │   ├── ocr.py
│   │   │   ├── pdf.py
│   │   │   └── routes.py
│   │   ├── data/
│   │   │   └── uploads/
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── db_service.py
│   │   │   ├── embedding_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── ocr_service.py
│   │   │   ├── pdf_service.py
│   │   │   ├── prompt_builder.py
│   │   │   ├── qa_service.py
│   │   │   ├── theme_detector.py
│   │   │   ├── theme_synthesizer.py
│   │   │   └── vector_store.py
│   │   ├── utils/
│   │   │   └── text_splitter.py
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
Setup and Installation
Pre-requisites
Docker and Docker Compose installed
Internet connection for downloading models and dependencies
Setup Steps
Clone the repository:
git clone <repository-url>
cd chatbot_theme_identifier
Create necessary directories:
mkdir -p backend/app/data/uploads
mkdir -p chroma_store
Start the services using Docker Compose:
docker-compose up -d
Download the Llama3 model for Ollama:
docker exec -it chatbot_theme_identifier-ollama-1 ollama pull llama3
Access the application:
Frontend UI: http://localhost:8501
Backend API: http://localhost:8000
API Documentation: http://localhost:8000/docs
Usage
Upload Documents:
Use the PDF Theme Extractor tab to upload PDF documents
Use the Image OCR tab to upload images for text extraction
Query Documents:
Use the LLaMA Chat tab to ask questions about the uploaded documents
Synthesize Themes:
Use the Synthesize Themes tab to identify common themes across documents
Features
Process 75+ documents (PDF, scanned images)
Extract text using OCR for scanned documents
Identify themes across documents
Query documents with LLaMA3 model
Get cited responses with document references
Technologies Used
Backend: FastAPI, Python
Frontend: Streamlit
LLM: Ollama (LLaMA3)
Vector Database: ChromaDB
Document Processing: PyMuPDF, Tesseract OCR
Database: MongoDB
