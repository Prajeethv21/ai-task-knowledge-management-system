from functools import lru_cache

from app.config.settings import settings


@lru_cache(maxsize=1)
def get_embedding_model():
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "sentence-transformers is not installed in the active environment. Install backend requirements before using semantic search."
        ) from exc

    return SentenceTransformer(settings.embedding_model)


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedding_model()
    return model.encode(texts, convert_to_numpy=True).tolist()
