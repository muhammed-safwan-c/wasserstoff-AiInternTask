import uuid
import chromadb
from chromadb.config import Settings
from app.services.embedding_service import get_embedding

# Initialize ChromaDB client
client = chromadb.Client(Settings(
    persist_directory="./chroma_store",  # Directory to store vectors
    anonymized_telemetry=False
))

# Custom embedding wrapper for Chroma
class SentenceTransformerEmbedding:
    def __call__(self, input: list) -> list:
        return [get_embedding(text) for text in input]

# Get or create ChromaDB collection
collection = client.get_or_create_collection(
    name="documents",
    embedding_function=SentenceTransformerEmbedding()
)

def chunk_text(text: str, chunk_size: int = 500) -> list:
    """
    Split text into chunks of roughly `chunk_size` words each.
    """
    words = text.split()
    chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def add_to_vectorstore(doc_id: str, text: str, metadata: dict = None):
    """
    Add document chunks to the ChromaDB vector store.
    """
    if not text.strip():
        print("[VectorDB] Empty text provided. Skipping...")
        return

    if metadata is None:
        metadata = {}

    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        uid = str(uuid.uuid4())
        chunk_metadata = {
            "doc_id": doc_id,
            "chunk_index": i,
            **metadata
        }
        try:
            collection.add(
                documents=[chunk],
                ids=[uid],
                metadatas=[chunk_metadata]
            )
        except Exception as e:
            print(f"[VectorDB] Error adding chunk {i}: {e}")

    print(f"[VectorDB] Stored {len(chunks)} chunks for doc_id={doc_id}")

def query_vectorstore(query: str, top_k: int = 5):
    """
    Search the ChromaDB vector store for the top_k most relevant chunks.
    Returns a dictionary with documents and their metadata.
    """
    if not query.strip():
        print("[VectorDB] Empty query provided.")
        return {}

    try:
        results = collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "metadatas"]
        )
        return results
    except Exception as e:
        print(f"[VectorDB] Query error: {e}")
        return {}
