

import csv
import os
from datetime import datetime


def ensure_parent(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def append_csv(path, row, fieldnames):
    ensure_parent(path)
    file_exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def log_retrieval(path, query, retrieved_chunks, final_prompt, answer):
    for rank, chunk in enumerate(retrieved_chunks, start=1):
        append_csv(
            path,
            {
                "timestamp": datetime.utcnow().isoformat(),
                "query": query,
                "rank": rank,
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "vector_score": chunk.get("vector_score", 0),
                "keyword_score": chunk.get("keyword_score", 0),
                "feedback_score": chunk.get("feedback_score", 0),
                "final_score": chunk.get("final_score", 0),
                "chunk_text": chunk["text"],
                "final_prompt": final_prompt,
                "answer": answer
            },
            [
                "timestamp", "query", "rank", "chunk_id", "source", "vector_score",
                "keyword_score", "feedback_score", "final_score", "chunk_text",
                "final_prompt", "answer"
            ]
        )


def log_feedback(path, query, chunk_id, feedback):
    append_csv(
        path,
        {
            "timestamp": datetime.utcnow().isoformat(),
            "query": query,
            "chunk_id": chunk_id,
            "feedback": feedback
        },
        ["timestamp", "query", "chunk_id", "feedback"]
    )


def read_feedback(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    import pandas as pd
    return pd.read_csv(path).fillna("").to_dict("records")
