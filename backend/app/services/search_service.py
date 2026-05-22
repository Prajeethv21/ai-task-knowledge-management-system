from app.ai.embedding_service import embed_texts
from app.ai.vector_store import vector_store


def semantic_search(query: str, top_k: int = 5) -> list[dict]:
    embedding = embed_texts([query])[0]
    return vector_store.search(embedding, top_k)
