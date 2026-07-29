import ollama
from .retrieval import retrieve


def build_prompt(chunks, user_prompt):

    context = ""

    for chunk in chunks:
        context += chunk["text"] + "\n\n"

    return f"""
You are an expert travel assistant.

Answer ONLY using the information provided.

If the information is insufficient, say so.

Context:

{context}

User Preference:

{user_prompt}

Write a concise travel summary in about 5 sentences.
"""


def generate_summary(city, user_prompt):

    if not user_prompt.strip():
        user_prompt = "General travel recommendations."

    chunks = retrieve(city, user_prompt)
    if not chunks:
        return "Travel details for this destination have not been added yet."
    prompt = build_prompt(chunks, user_prompt)

    response = ollama.chat(
        model="hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF:latest",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]

if __name__ == "__main__":

    summary = generate_summary(
        "Kyoto",
        "I like photography and quiet places."
    )

    print(summary)