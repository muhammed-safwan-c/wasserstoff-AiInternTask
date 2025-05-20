import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

# Primary and fallback model names
PRIMARY_MODEL = "llama3"
FALLBACK_MODEL = "tinyllama"  # lightweight, less RAM needed

def call_llm(prompt: str) -> str:
    """
    Calls Ollama with the prompt. If the primary model fails, falls back to a lighter one.
    Returns a clean string response.
    """
    def send_prompt(model_name: str) -> str:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(OLLAMA_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                return f"LLM Error from {model_name}: {data['error']}"

            answer = data.get("response", "").strip()
            return answer or f"LLM responded with an empty result using {model_name}."

        except requests.exceptions.ConnectionError:
            return "❌ LLM Connection Error: Is Ollama running at localhost:11434?"

        except requests.exceptions.RequestException as e:
            return f"❌ LLM Request Error ({model_name}): {str(e)}"

    # Step 1: Try primary model
    print(f"🧠 Calling primary model: {PRIMARY_MODEL}")
    response = send_prompt(PRIMARY_MODEL)

    # Step 2: If memory or server error, fallback to tiny model
    if "requires more system memory" in response or "LLM Error" in response:
        print(f"⚠️ Primary model failed. Switching to fallback model: {FALLBACK_MODEL}")
        fallback_response = send_prompt(FALLBACK_MODEL)
        return fallback_response

    return response
