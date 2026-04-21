
import os
from openai import OpenAI


def generate_answer(prompt, context=""):
    """Generate the final answer from the retrieved evidence.

    The OpenAI call is used for generation only. Retrieval, context selection,
    and prompt construction are implemented manually in this project.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return fallback_answer(context)

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a careful Academic City RAG assistant. Answer only from retrieved evidence. If the context is insufficient, say so."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as exc:
        return (
            f"The LLM generation step failed: {exc}\n\n"
            "Fallback answer from retrieved context:\n\n"
            + fallback_answer(context)
        )


def fallback_answer(context):
    if not context or not context.strip():
        return "I could not find this information in the retrieved documents."
    shortened = context.strip()
    if len(shortened) > 1800:
        shortened = shortened[:1800] + "..."
    return "Based on the retrieved context:\n\n" + shortened
