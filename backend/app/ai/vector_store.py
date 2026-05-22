import json
import os
from typing import List

try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    faiss = None
    FAISS_AVAILABLE = False
import numpy as np

from app.config.settings import settings
from app.utils.text_chunker import normalize_text, text_fingerprint


class VectorStore:
    def __init__(self) -> None:
        self.index_path = os.path.join(settings.vector_dir, "faiss.index")
        self.meta_path = os.path.join(settings.vector_dir, "metadata.json")
        self._index = None
        self._metadata: list[dict] = []
        self._dim = None
        self._ensure_dirs()
        self._load()

    def _ensure_dirs(self) -> None:
        os.makedirs(settings.vector_dir, exist_ok=True)

    def _load(self) -> None:
        if os.path.exists(self.index_path) and os.path.exists(self.meta_path):
            if FAISS_AVAILABLE:
                self._index = faiss.read_index(self.index_path)
            else:
                # fallback: load numpy vectors as plain file if present
                try:
                    self._index = np.load(self.index_path + ".npy")
                except Exception:
                    self._index = None
            with open(self.meta_path, "r", encoding="utf-8") as handle:
                self._metadata = json.load(handle)
            if FAISS_AVAILABLE and self._index is not None:
                self._dim = self._index.d
            elif isinstance(self._index, np.ndarray):
                self._dim = int(self._index.shape[1])

    def _init_index(self, dim: int) -> None:
        if FAISS_AVAILABLE:
            self._index = faiss.IndexFlatIP(dim)
        else:
            # fallback: use list to store vectors
            self._index = np.empty((0, dim), dtype="float32")
        self._dim = dim

    def add_texts(
        self,
        embeddings: List[List[float]],
        metadata: List[dict],
        documents: List[str],
        ids: List[str],
    ) -> None:
        if not embeddings:
            return
        existing_hashes = {item.get("text_hash") for item in self._metadata}
        filtered_embeddings = []
        filtered_metadata = []
        filtered_documents = []
        filtered_ids = []

        for embedding, meta, text, chunk_id in zip(embeddings, metadata, documents, ids):
            text_hash = meta.get("text_hash") or text_fingerprint(text)
            if text_hash in existing_hashes:
                continue
            existing_hashes.add(text_hash)
            meta["text_hash"] = text_hash
            filtered_embeddings.append(embedding)
            filtered_metadata.append(meta)
            filtered_documents.append(text)
            filtered_ids.append(chunk_id)

        if not filtered_embeddings:
            return

        vectors = np.array(filtered_embeddings).astype("float32")
        # normalize for cosine similarity
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        if self._index is None:
            self._init_index(vectors.shape[1])
        enriched_meta = []
        for item, text, chunk_id in zip(filtered_metadata, filtered_documents, filtered_ids):
            enriched_meta.append({"text": text, **item, "chunk_store_id": chunk_id})
        if FAISS_AVAILABLE:
            self._index.add(vectors)
        else:
            self._index = np.vstack([self._index, vectors]) if self._index.size else vectors
        self._metadata.extend(enriched_meta)
        self._persist()

    def _is_near_duplicate(self, text_a: str, text_b: str, threshold: float = 0.92) -> bool:
        tokens_a = set(normalize_text(text_a).split())
        tokens_b = set(normalize_text(text_b).split())
        if not tokens_a or not tokens_b:
            return False
        overlap = len(tokens_a & tokens_b)
        score = overlap / max(len(tokens_a), len(tokens_b))
        return score >= threshold

    def search(self, embedding: List[float], top_k: int = 5) -> List[dict]:
        if self._index is None or not self._metadata:
            return []
        vector = np.array(embedding).astype("float32")
        vector = vector / np.linalg.norm(vector)
        results = []
        desired = max(top_k * 5, top_k)
        if FAISS_AVAILABLE:
            q = np.array([vector])
            faiss.normalize_L2(q)
            scores, indices = self._index.search(q, desired)
            for score, idx in zip(scores[0], indices[0]):
                if idx < 0 or idx >= len(self._metadata):
                    continue
                meta = self._metadata[idx]
                results.append({"score": float(score), **meta})
        else:
            # brute-force cosine similarity search
            if len(self._index) == 0:
                return []
            sims = (self._index @ vector).tolist()
            ranked = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)[:desired]
            for idx, score in ranked:
                meta = self._metadata[idx]
                results.append({"score": float(score), **meta})

        deduped = []
        seen_hashes = set()
        for item in results:
            text = item.get("text") or ""
            text_hash = item.get("text_hash") or hash(normalize_text(text))
            if text_hash in seen_hashes:
                continue
            if any(self._is_near_duplicate(text, existing.get("text", "")) for existing in deduped):
                continue
            seen_hashes.add(text_hash)
            deduped.append(item)
            if len(deduped) >= top_k:
                break

        return deduped

    def _persist(self) -> None:
        if self._index is None:
            return
        if FAISS_AVAILABLE:
            faiss.write_index(self._index, self.index_path)
        else:
            # save numpy array
            try:
                np.save(self.index_path + ".npy", self._index)
            except Exception:
                pass
        with open(self.meta_path, "w", encoding="utf-8") as handle:
            json.dump(self._metadata, handle)

    def reset(self) -> None:
        self._index = None
        self._metadata = []
        self._dim = None
        if os.path.exists(self.index_path):
            try:
                os.remove(self.index_path)
            except Exception:
                pass
        if os.path.exists(self.index_path + ".npy"):
            try:
                os.remove(self.index_path + ".npy")
            except Exception:
                pass
        if os.path.exists(self.meta_path):
            try:
                os.remove(self.meta_path)
            except Exception:
                pass


vector_store = VectorStore()
