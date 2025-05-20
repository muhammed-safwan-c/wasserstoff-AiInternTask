def build_prompt(query: str, document_snippets: list[str]) -> str:
    """
    Constructs a prompt string for the LLM to synthesize themes
    based on the user's query and relevant document text snippets.

    Args:
        query (str): The user's natural language query.
        document_snippets (list[str]): List of extracted text snippets from documents
                                       relevant to the query.

    Returns:
        str: A formatted prompt string for the language model.
    """
    # Combine snippets into a single context block
    context = "\n\n---\n\n".join(document_snippets)

    prompt = (
        f"User Query:\n{query}\n\n"
        "Documents Content:\n"
        f"{context}\n\n"
        "Please analyze the above documents, identify common themes related to the user's query, "
        "and provide a detailed, cited synthesis response. List themes clearly and cite document sources "
        "where applicable."
    )
    return prompt
