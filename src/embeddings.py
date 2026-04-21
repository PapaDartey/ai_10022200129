

import numpy as np
from sentence_transformers import SentenceTransformer


class EmbeddingPipeline:
    """Manual embedding pipeline using SentenceTransformers."""
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.astype("float32")

    def embed_query(self, query):
        return self.embed_texts([query])[0]
