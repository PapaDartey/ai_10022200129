

STRICT_PROMPT_TEMPLATE = """You are an Academic City AI assistant answering questions using only the retrieved context.

Rules:
1. Use only the provided context.
2. If the answer is not in the context, say: "I could not find this information in the provided documents."
3. Do not invent figures, dates, parties, regions, or policy statements.
4. Cite the source type as either Election Dataset or Budget Statement.
5. Give a clear and concise answer.

Retrieved Context:
{context}

User Question:
{query}

Answer:
"""


BASIC_PROMPT_TEMPLATE = """Answer the question using the context below.

Context:
{context}

Question:
{query}

Answer:
"""


def format_context(chunks):
    lines = []
    for i, chunk in enumerate(chunks, start=1):
        lines.append(
            f"[{i}] Source: {chunk['source']} | Chunk ID: {chunk['chunk_id']} | "
            f"Score: {chunk.get('final_score', 0):.4f}\n{chunk['text']}"
        )
    return "\n\n".join(lines)


def build_prompt(query, chunks, strict=True):
    context = format_context(chunks)
    template = STRICT_PROMPT_TEMPLATE if strict else BASIC_PROMPT_TEMPLATE
    return template.format(context=context, query=query)
