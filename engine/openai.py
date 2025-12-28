import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"

def generate_answer(question: str, documents: list[str]) -> str:
    if not documents:
        return "No relevant documents found to answer the question."

    context = "\n".join(documents)

    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the information below.
If the answer is not present, say you do not know.

Documents:
{context}

Question:
{question}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()
    return data["message"]["content"].strip()