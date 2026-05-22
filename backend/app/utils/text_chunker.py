import hashlib
import re
from typing import List


def normalize_text(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text or "").strip()
    return normalized


def text_fingerprint(text: str) -> str:
    normalized = normalize_text(text)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def chunk_text(text: str, chunk_size: int = 700, overlap_sentences: int = 1) -> List[str]:
    normalized = normalize_text(text)
    if not normalized:
        return []

    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", normalized) if s.strip()]
    chunks: List[str] = []
    current: List[str] = []
    seen = set()

    def flush_chunk():
        if not current:
            return
        chunk = " ".join(current).strip()
        if chunk and chunk not in seen:
            chunks.append(chunk)
            seen.add(chunk)

    for sentence in sentences:
        candidate = " ".join(current + [sentence]).strip()
        if len(candidate) <= chunk_size:
            current.append(sentence)
            continue

        flush_chunk()
        if overlap_sentences > 0:
            current = current[-overlap_sentences:]
        else:
            current = []

        if sentence:
            current.append(sentence)

    flush_chunk()
    return chunks
