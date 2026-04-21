

import faiss
import numpy as np


class VectorStore:
    """Manual FAISS vector store wrapper."""
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatIP(dimension)
        self.chunks = []

    def add(self, embeddings, chunks):
        if len(embeddings) != len(chunks):
            raise ValueError("Number of embeddings must match number of chunks")
        self.index.add(np.array(embeddings).astype("float32"))
        self.chunks.extend(chunks)

    def search(self, query_embedding, top_k=5):
        query_embedding = np.array([query_embedding]).astype("float32")
        scores, indices = self.index.search(query_embedding, top_k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            item = self.chunks[int(idx)].copy()
            item["vector_score"] = float(score)
            results.append(item)
        return results
