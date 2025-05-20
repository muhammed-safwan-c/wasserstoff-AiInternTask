import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend', 'app', 'services')))

from embedding_service import get_embedding
from vector_store import SentenceTransformerEmbedding, add_to_vectorstore, query_vectorstore


if __name__ == "__main__":
    sample_text = "This is a test sentence to embed."
    
    # Test embedding service directly
    embedding = get_embedding(sample_text)
    print(f"Embedding vector length: {len(embedding)}")  # should print 384 for all-MiniLM-L6-v2
    
    # Test your embedding function wrapper
    embedding_func = SentenceTransformerEmbedding()
    batch_embeddings = embedding_func([sample_text, sample_text])
    print(f"Batch embeddings count: {len(batch_embeddings)}")  # should print 2
    print(f"Length of first embedding vector: {len(batch_embeddings[0])}")
    
    # Test chunking and adding to vectorstore (assuming collection is set)
    add_to_vectorstore("doc1", sample_text)
    
    # Query the vector store
    results = query_vectorstore("test")
    print(results)
