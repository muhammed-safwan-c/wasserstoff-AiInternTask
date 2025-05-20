from app.services.vector_store import query_vectorstore
from app.services.llm_service import call_llm


def build_prompt(query: str, chunks: list[str], metadatas: list[dict]) -> str:
    """
    Constructs a prompt for the LLM using query and top relevant chunks.
    """
    context = ""
    for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
        doc_id = meta.get("doc_id", "Unknown")
        chunk_index = meta.get("chunk_index", "?")
        citation = f"[Doc ID: {doc_id}, Chunk: {chunk_index}]"
        context += f"{citation}\n{chunk.strip()}\n\n"

    prompt = f"""You are a document research assistant. Use the context below to answer the user query. 
Provide a concise and factual answer with citations in [Doc ID, Chunk] format.

### Context:
{context}

### User Question:
{query}

### Answer:"""

    return prompt


def answer_query(query: str, top_k: int = 5) -> dict:
    """
    Orchestrates the process: vector search → prompt → LLM → answer.
    """
    print(f"[QA] Received query: {query}")
    
    results = query_vectorstore(query, top_k=top_k)
    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    if not documents or not documents[0]:
        print("[QA] No relevant chunks found.")
        return {"answer": "Sorry, I couldn't find any relevant information.", "citations": []}

    chunks = documents[0]
    meta_list = metadatas[0] if metadatas else [{}] * len(chunks)

    print(f"[QA] Retrieved {len(chunks)} chunks.")
    
    prompt = build_prompt(query, chunks, meta_list)
    print(f"[QA] Prompt preview:\n{prompt[:500]}...\n---")  # Preview the first 500 chars

    try:
        answer = call_llm(prompt)
    except Exception as e:
        print(f"[QA] Error calling LLM: {e}")
        return {"answer": "An error occurred while processing your question.", "citations": []}

    return {
        "query": query,
        "answer": answer,
        "citations": meta_list
    }
