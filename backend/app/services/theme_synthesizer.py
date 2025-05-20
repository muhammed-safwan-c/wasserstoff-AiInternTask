from app.services.vector_store import query_vectorstore as similarity_search
from app.services.llm_service import call_llm
import logging

logger = logging.getLogger(__name__)

def synthesize_themes(user_query: str):
    results = similarity_search(user_query)

    chunks = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    if not chunks:
        return {
            "query": user_query,
            "themes": "⚠️ No relevant content found for synthesis."
        }

    context_blocks = []

    for chunk, meta in zip(chunks, metadatas):
        doc_id = meta.get("doc_id", "UnknownDoc")
        context_blocks.append(f"[{doc_id}] {chunk.strip()}")

    context = "\n\n".join(context_blocks)

    theme_prompt = f"""
You are a legal/document analyst bot.

Given the following responses from documents related to the query: **{user_query}**

Identify common themes, and cite supporting documents using [DocumentID] tags.

--- Start of Responses ---
{context}
--- End of Responses ---

Output Format:
Theme 1 – [Theme Name]:
[Brief explanation]
Documents: [Document IDs]

Theme 2 – ...
"""

    try:
        response = call_llm(theme_prompt)
    except Exception as e:
        logger.error(f"LLM Error: {e}")
        response = "⚠️ Error generating themes."

    return {
        "query": user_query,
        "themes": response.strip()
    }
