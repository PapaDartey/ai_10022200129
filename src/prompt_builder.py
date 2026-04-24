STRICT_PROMPT_TEMPLATE = """You are an Academic City AI assistant answering questions using only the retrieved context.

Rules:
1. Use only the provided context.
2. If the answer is not in the context, say exactly: "I couldn’t find a reliable answer to that in the available data. Try rephrasing your question or asking about a related topic"
3. Do not invent figures, dates, parties, regions, policy statements, winners, or summaries.
4. Cite the source type as either Election Dataset or Budget Statement.
5. Give a clear and concise answer.
6. Do not infer a national election winner from regional results alone.
7. Only state a national winner if the retrieved context explicitly contains a national summary or a clearly aggregated national result.
8. If the context contains only regional results and the user asks a national question, say that the retrieved context does not clearly provide the national result.
9. If multiple retrieved chunks conflict or point to different regions or candidates, do not guess. State that the context is insufficient or mixed.

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