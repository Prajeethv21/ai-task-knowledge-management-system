import os
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.ai.embedding_service import embed_texts
from app.ai.vector_store import vector_store
from app.config.settings import settings
from app.models.document import Document
from app.utils.text_chunker import chunk_text, text_fingerprint


def save_document(db: Session, file: UploadFile, uploaded_by: int) -> Document:
    if file.content_type != "text/plain" or not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    os.makedirs(settings.upload_dir, exist_ok=True)
    filename = f"{uploaded_by}_{file.filename}"
    file_path = os.path.join(settings.upload_dir, filename)
    content = file.file.read().decode("utf-8", errors="ignore")

    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(content)

    chunks = chunk_text(content)

    document = Document(
        filename=filename,
        original_name=file.filename,
        content_type=file.content_type,
        size=len(content.encode("utf-8")),
        chunk_count=len(chunks),
        uploaded_by=uploaded_by,
    )
    db.add(document)
    db.commit()
    db.refresh(document)

    metadata = []
    for idx, chunk in enumerate(chunks):
        metadata.append(
            {
                "document_id": document.id,
                "chunk_id": idx,
                "document_name": document.original_name,
                "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else "",
                "text_hash": text_fingerprint(chunk),
                "preview": chunk[:200],
            }
        )

    embeddings = embed_texts(chunks)

    ids = [f"doc_{document.id}_chunk_{idx}" for idx in range(len(chunks))]
    vector_store.add_texts(embeddings, metadata, chunks, ids)
    return document


def list_documents(db: Session) -> list[Document]:
    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


def rebuild_index(db: Session) -> None:
    documents = db.query(Document).order_by(Document.uploaded_at.asc()).all()
    vector_store.reset()
    for document in documents:
        file_path = os.path.join(settings.upload_dir, document.filename)
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
            content = handle.read()
        chunks = chunk_text(content)
        if not chunks:
            continue
        metadata = []
        for idx, chunk in enumerate(chunks):
            metadata.append(
                {
                    "document_id": document.id,
                    "chunk_id": idx,
                    "document_name": document.original_name,
                    "uploaded_at": document.uploaded_at.isoformat() if document.uploaded_at else "",
                    "text_hash": text_fingerprint(chunk),
                    "preview": chunk[:200],
                }
            )
        embeddings = embed_texts(chunks)
        ids = [f"doc_{document.id}_chunk_{idx}" for idx in range(len(chunks))]
        vector_store.add_texts(embeddings, metadata, chunks, ids)


def delete_document(db: Session, document_id: int) -> None:
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = os.path.join(settings.upload_dir, document.filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass

    db.delete(document)
    db.commit()
    rebuild_index(db)
