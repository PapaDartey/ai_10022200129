import re
from collections import Counter


def tokenize(text):
    return re.findall(r"[A-Za-z0-9]+", text.lower())


def keyword_overlap_score(query, text):
    q_tokens = Counter(tokenize(query))
    t_tokens = Counter(tokenize(text))
    if not q_tokens:
        return 0.0
    overlap = sum(min(q_tokens[token], t_tokens.get(token, 0)) for token in q_tokens)
    return overlap / max(1, sum(q_tokens.values()))


def feedback_adjustment(chunk, feedback_records):
    """Boost or reduce a chunk score using previous feedback."""
    chunk_id = chunk.get("chunk_id", "")
    relevant = sum(
        1 for row in feedback_records
        if row.get("chunk_id") == chunk_id and row.get("feedback") == "Relevant"
    )
    irrelevant = sum(
        1 for row in feedback_records
        if row.get("chunk_id") == chunk_id and row.get("feedback") == "Not relevant"
    )
    return 0.05 * relevant - 0.05 * irrelevant


def is_national_winner_query(query):
    q = query.lower().strip()

    national_patterns = [
        "who won the 2020 election",
        "who won the election",
        "who won the national election",
        "who won ghana election",
        "national winner",
        "winner of the election",
        "winner of the 2020 election",
        "president of ghana",
        "who is the president",
        "current president",
        "who won the presidential election",
    ]

    return any(pattern in q for pattern in national_patterns)


def is_regional_query(query):
    q = query.lower()
    regional_markers = [
        "region",
        "greater accra",
        "ashanti",
        "ahafo",
        "bono",
        "bono east",
        "central",
        "eastern",
        "north east",
        "northern",
        "oti",
        "savannah",
        "upper east",
        "upper west",
        "volta",
        "western",
        "western north",
    ]
    return any(marker in q for marker in regional_markers)


def domain_score_adjustment(query, chunk):
    """
    Boost chunks based on the type of question being asked.
    This helps broad national questions retrieve national summary chunks
    instead of mixed regional rows.
    """
    metadata = chunk.get("metadata", {})
    chunk_type = metadata.get("chunk_type", "")

    national_query = is_national_winner_query(query)
    regional_query = is_regional_query(query)

    boost = 0.0

    if national_query:
        if chunk_type == "national_summary":
            boost += 0.20
        elif chunk_type == "national_summary_helper":
            boost += 0.15
        elif chunk_type == "regional_summary":
            boost -= 0.08
        elif chunk_type == "row_result":
            boost -= 0.05

    if regional_query:
        if chunk_type == "regional_summary":
            boost += 0.12
        elif chunk_type == "national_summary":
            boost -= 0.05

    return boost


def hybrid_retrieve(
    query,
    embedding_pipeline,
    vector_store,
    top_k=5,
    vector_weight=0.75,
    keyword_weight=0.25,
    feedback_records=None
):
    """Manual retrieval with vector similarity plus keyword overlap and domain-aware boosting."""
    feedback_records = feedback_records or []
    query_embedding = embedding_pipeline.embed_query(query)
    vector_results = vector_store.search(query_embedding, top_k=max(top_k * 4, 10))

    rescored = []
    for item in vector_results:
        key_score = keyword_overlap_score(query, item["text"])
        fb_score = feedback_adjustment(item, feedback_records)
        domain_score = domain_score_adjustment(query, item)

        final_score = (
            (vector_weight * item["vector_score"])
            + (keyword_weight * key_score)
            + fb_score
            + domain_score
        )

        item["keyword_score"] = float(key_score)
        item["feedback_score"] = float(fb_score)
        item["domain_score"] = float(domain_score)
        item["final_score"] = float(final_score)
        rescored.append(item)

    rescored.sort(key=lambda x: x["final_score"], reverse=True)
    return rescored[:top_k]


def select_context(retrieved_chunks, max_words=1200):
    selected = []
    used_words = 0

    for chunk in retrieved_chunks:
        words = chunk["text"].split()
        if used_words + len(words) > max_words:
            remaining = max_words - used_words
            if remaining > 40:
                shortened = chunk.copy()
                shortened["text"] = " ".join(words[:remaining])
                selected.append(shortened)
            break

        selected.append(chunk)
        used_words += len(words)

    return selected