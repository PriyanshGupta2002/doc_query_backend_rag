from sentence_transformers import SentenceTransformer
from typing import List

_model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def embed_documents(texts: List[str]):
    return _model.encode(
        texts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True  # 🔥 important for cosine similarity
    )


def embed_query(query: str):
    return _model.encode(
        query,
        normalize_embeddings=True
    )