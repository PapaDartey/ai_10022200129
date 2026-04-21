

from .retrieval import hybrid_retrieve, select_context
from .prompt_builder import build_prompt
from .generator import generate_answer


ADVERSARIAL_QUERIES = [
    {
        "query": "Who won in the region?",
        "type": "Ambiguous query",
        "expected": "The system should ask for the region or state that the information is not specific enough."
    },
    {
        "query": "How many votes did the Labour Party get in Ahafo in 2020?",
        "type": "Misleading query",
        "expected": "The system should not invent a Labour Party result if it is not in the retrieved evidence."
    }
]


def run_single_rag_test(query, embedding_pipeline, vector_store, feedback_records=None):
    retrieved = hybrid_retrieve(query, embedding_pipeline, vector_store, feedback_records=feedback_records)
    context = select_context(retrieved)
    prompt = build_prompt(query, context, strict=True)
    answer = generate_answer(prompt)
    return {
        "query": query,
        "retrieved": retrieved,
        "prompt": prompt,
        "answer": answer
    }
